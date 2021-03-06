from django.utils.decorators import method_decorator

from apps.cliente.models import Cliente
from apps.mixins import ValidatePermissionRequiredMixin
import json
from datetime import datetime

from django.db import transaction
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.cliente.forms import ClienteForm
from apps.producto_base.models import Producto_base
from apps.reparacion.forms import ReparacionForm, Detalle_reparacionform
from apps.reparacion.models import Reparacion, Detalle_reparacion
from apps.empresa.models import Empresa


import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from apps.transaccion.forms import TransaccionForm
from apps.transaccion.models import Transaccion
from apps.user.models import User

opc_icono = 'fas fa-tools'
opc_entidad = 'Reparaciones'
crud = '/reparacion/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Reparacion
    template_name = 'front-end/reparacion/reparacion_list.html'
    permission_required = 'reparacion.view_reparacion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'reparacion':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start == '' and end == '':
                    query = Reparacion.objects.filter(transaccion__tipo=1)
                else:
                    query = Reparacion.objects.filter(transaccion__tipo=1, transaccion__fecha_trans__range=[start, end])
                for c in query:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    result = Detalle_reparacion.objects.filter(reparacion_id=id)
                    for p in result:
                        data.append({
                            'producto': p.producto.producto_base.nombre,
                            'categoria': p.producto.producto_base.categoria.nombre,
                            'presentacion': p.producto.producto_base.presentacion.nombre,
                            'cantidad': p.cantidad,
                            'pvp': p.pvp_rep_by_prod,
                            'subtotal': p.subtotal
                        })
            elif action == 'anular':
                id = request.POST['id']
                result = Reparacion.objects.get(id=id)
                result.estado = 2
                result.save()
                data['resp'] = True
            elif action == 'entregar':
                id = request.POST['id']
                result = Reparacion.objects.get(id=id)
                result.estado = 1
                result.fecha_entrega = datetime.now()
                result.save()
                data['resp'] = True
            elif action == 'estado':
                id = request.POST['id']
                result = Reparacion.objects.get(id=id)
                result.fecha_ingreso = datetime.now()
                result.estado = 0
                result.save()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Reparacion'
        data['titulo'] = 'Listado de Reparaciones'
        data['nuevo'] = '/reparacion/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Reparacion
    template_name = 'front-end/reparacion/reparacion_form.html'
    permission_required = 'reparacion.add_reparacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                datos = json.loads(request.POST['reparacion'])
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = datos['cliente']
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 1
                        c.save()
                        v = Reparacion()
                        v.transaccion_id = c.id
                        v.fecha_ingreso = datos['fecha_ingreso']
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dv = Detalle_reparacion()
                                dv.reparacion_id = v.id
                                dv.producto_id = int(i['id'])
                                dv.cantidad = int(i['cantidad'])
                                dv.pvp_rep_by_prod = float(i['pvp'])
                                dv.subtotal = float(i['subtotal'])
                                dv.save()
                        data['id'] = v.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Repararcion'
        data['titulo'] = 'Nueva Repararcion'
        data['nuevo'] = '/reparacion/nuevo'
        data['empresa'] = empresa
        data['form'] = TransaccionForm()
        data['formr'] = ReparacionForm()
        data['form2'] = Detalle_reparacionform()
        data['detalle'] = []
        data['formc'] = ClienteForm()
        return data


class CrudViewOnline(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Reparacion
    template_name = 'front-end/reparacion/reparacion_online.html'
    permission_required = 'reparacion.add_reparacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            datos = json.loads(request.POST['reparacion'])
            us = User.objects.get(id=request.user.id)
            cli = Cliente.objects.get(cedula=us.cedula)
            if action == 'add':
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = cli.id
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 1
                        c.save()
                        v = Reparacion()
                        v.transaccion_id = c.id
                        v.fecha_ingreso = datos['fecha_ingreso']
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dv = Detalle_reparacion()
                                dv.reparacion_id = v.id
                                dv.producto_id = int(i['id'])
                                dv.cantidad = int(i['cantidad'])
                                dv.pvp_rep_by_prod = float(i['pvp'])
                                dv.subtotal = float(i['subtotal'])
                                dv.save()
                        data['id'] = v.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'reserva':
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = cli.id
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 1
                        c.save()
                        v = Reparacion()
                        v.transaccion_id = c.id
                        v.estado = 3
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dv = Detalle_reparacion()
                                dv.reparacion_id = v.id
                                dv.producto_id = int(i['id'])
                                dv.cantidad = int(i['cantidad'])
                                dv.pvp_rep_by_prod = float(i['pvp'])
                                dv.subtotal = float(i['subtotal'])
                                dv.save()
                        data['id'] = v.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Nueva Reparacion'
        data['empresa'] = empresa
        data['form'] = TransaccionForm()
        data['form2'] = Detalle_reparacionform()
        data['detalle'] = []
        user = Cliente.objects.get(cedula=self.request.user.cedula)
        data['formc'] = ClienteForm(instance=user)
        return data


class printpdf(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def pvp_cal(self, *args, **kwargs):
        data = []
        try:
            for i in Detalle_reparacion.objects.filter(reparacion_id=self.kwargs['pk']):
                item = i.reparacion.toJSON()
                item['producto'] = {'producto': i.producto.toJSON()}
                item['pvp'] = format(i.pvp_rep_by_prod, '.2f')
                item['cantidad'] = i.cantidad
                item['subtotal'] = i.subtotal
                data.append(item)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf.html')
            context = {'title': 'Comprobante de Reparacion',
                       'sale': Reparacion.objects.get(pk=self.kwargs['pk']),
                       'det_sale': self.pvp_cal(),
                       'empresa': Empresa.objects.first(),
                       'icon': 'media/imagen.PNG',
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('reparacion:lista'))


class report(ValidatePermissionRequiredMixin, ListView):
    model = Reparacion
    template_name = 'front-end/reparacion/reparacion_report_product.html'
    permission_required = 'reparacion.view_reparacion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reparacion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Detalle_reparacion.objects.values('reparacion__transaccion__fecha_trans',
                                                         'producto__producto_base_id',
                                                         'pvp_rep_by_prod').order_by().annotate(
                        Sum('cantidad')).filter(reparacion__estado=1)
                else:
                    query = Detalle_reparacion.objects.values('reparacion__transaccion__fecha_trans',
                                                         'producto__producto_base_id',
                                                         'pvp_rep_by_prod') \
                        .filter(reparacion__transaccion__fecha_trans__range=[start_date, end_date],
                                reparacion__estado=1).order_by().annotate(
                        Sum('cantidad'))
                for p in query:
                    total = p['pvp_rep_by_prod'] * p['cantidad__sum']
                    pr = Producto_base.objects.get(id=int(p['producto__producto_base_id']))
                    data.append([
                        p['reparacion__transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        pr.nombre,
                        int(p['cantidad__sum']),
                        format(p['pvp_rep_by_prod'], '.2f'),
                        format(total, '.2f'),
                        format((float(total) * iva), '.2f'),
                        format(((float(total) * iva) + float(total)), '.2f')
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Reparacion de prendas'
        data['empresa'] = empresa
        return data


class report_total(ValidatePermissionRequiredMixin, ListView):
    model = Reparacion
    template_name = 'front-end/reparacion/reparacion_report_total.html'
    permission_required = 'reparacion.view_reparacion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reparacion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Reparacion.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos', 'transaccion__user__username')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=1)
                else:
                    query = Reparacion.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos',
                                                 'transaccion__user__username').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=1). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__cliente__nombres'] + " " + p['transaccion__cliente__apellidos'],
                        p['transaccion__user__username'],
                        format(p['transaccion__subtotal__sum'], '.2f'),
                        format((p['transaccion__iva__sum']), '.2f'),
                        format(p['transaccion__total__sum'], '.2f')
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Reparacion de prendas'
        data['titulo'] = 'Reporte de reparacion de prendas'
        data['empresa'] = empresa
        return data


class report_total_alquilada(ValidatePermissionRequiredMixin, ListView):
    model = Reparacion
    template_name = 'front-end/reparacion/reparacion_report_total_alquiladas.html'
    permission_required = 'reparacion.view_reparacion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reparacion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Reparacion.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos', 'transaccion__user__username')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=0)
                else:
                    query = Reparacion.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos',
                                                 'transaccion__user__username').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=0). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__cliente__nombres'] + " " + p['transaccion__cliente__apellidos'],
                        p['transaccion__user__username'],
                        format(p['transaccion__subtotal__sum'], '.2f'),
                        format((p['transaccion__iva__sum']), '.2f'),
                        format(p['transaccion__total__sum'], '.2f')
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Reparacion de prendas/No entregadas'
        data['titulo'] = 'Reporte de reparacion de prendas'
        data['empresa'] = empresa
        return data


class report_total_reservada(ValidatePermissionRequiredMixin, ListView):
    model = Reparacion
    template_name = 'front-end/reparacion/reparacion_report_total_reservadas.html'
    permission_required = 'reparacion.view_reparacion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reparacion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Reparacion.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos', 'transaccion__user__username')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=3)
                else:
                    query = Reparacion.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos',
                                                 'transaccion__user__username').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=3). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__cliente__nombres'] + " " + p['transaccion__cliente__apellidos'],
                        p['transaccion__user__username'],
                        format(p['transaccion__subtotal__sum'], '.2f'),
                        format((p['transaccion__iva__sum']), '.2f'),
                        format(p['transaccion__total__sum'], '.2f')
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Reparacion de prendas/Reservadas'
        data['titulo'] = 'Reporte de reparacion de prendas'
        data['empresa'] = empresa
        return data
