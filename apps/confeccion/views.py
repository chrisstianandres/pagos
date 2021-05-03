import json
import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles import finders
from django.db import transaction
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from xhtml2pdf import pisa

from apps.asignar_recursos.models import Asig_recurso, Detalle_produccion
from apps.backEnd import nombre_empresa, verificar
from apps.cliente.forms import ClienteForm
from apps.cliente.models import Cliente
from apps.confeccion.forms import ConfeccionForm, Detalle_confeccionform
from apps.confeccion.models import Confeccion, Detalle_confeccion
from apps.empresa.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.models import Producto
from apps.producto_base.models import Producto_base
from apps.transaccion.forms import TransaccionForm
from apps.transaccion.models import Transaccion
from apps.user.forms import UserForm
from apps.user.models import User

opc_icono = 'fab fa-shirtsinbulk'
opc_entidad = 'Confeccion para clientes'
crud = '/confeccion/crear'
empresa = nombre_empresa()
year = [{'id': y, 'year': (datetime.now().year)-y}for y in range(0, 5)]


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Confeccion
    template_name = 'front-end/confeccion/confeccion_list.html'
    permission_required = 'confeccion.view_confeccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'confeccion':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start == '' and end == '':
                    query = Confeccion.objects.filter(transaccion__tipo=3)
                else:
                    query = Confeccion.objects.filter(transaccion__tipo=3, transaccion__fecha_trans__range=[start, end])
                for c in query:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    result = Detalle_confeccion.objects.filter(producto__asignacion_id=id)
                    for p in result:
                        data.append({
                            'producto': p.producto.producto.producto_base.nombre,
                            'categoria': p.producto.producto.producto_base.categoria.nombre,
                            'color': p.producto.producto.color.nombre,
                            'talla': p.producto.producto.talla.talla_full(),
                            'cantidad': p.producto.cantidad,
                            'pvp': p.pvp_by_confec,
                            'subtotal': p.subtotal
                        })
            elif action == 'anular':
                id = request.POST['id']
                result = Confeccion.objects.get(id=id)
                result.estado = 2
                result.save()
                asignar = Asig_recurso.objects.get(id=result.confeccion_id)
                if asignar.estado == 1:
                    asignar.estado = 0
                    asignar.save()
                elif asignar.estado == 2:
                    for d in asignar.detalle_produccion_set.all():
                        prd = Producto.objects.get(id=d.producto.id)
                        prd.stock += d.cantidad
                        prd.save()
                data['resp'] = True
            elif action == 'entregar':
                id = request.POST['id']
                result = Confeccion.objects.get(id=id)
                result.estado = 1
                result.fecha_entrega = datetime.now()
                result.save()
                data['resp'] = True
            elif action == 'estado':
                id = request.POST['id']
                result = Confeccion.objects.get(id=id)
                result.estado = 0
                result.save()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Confeccion'
        data['titulo'] = 'Listado de Confecciones para Clientes'
        data['nuevo'] = '/confeccion/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Confeccion
    template_name = 'front-end/confeccion/confeccion_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                datos = json.loads(request.POST['confeccion'])
                if datos:
                    with transaction.atomic():
                        asig = Asig_recurso()
                        asig.fecha_asig = datos['fecha_venta']
                        asig.user_id = datos['cliente']
                        asig.save()
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.user_id = datos['cliente']
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 3
                        c.save()
                        v = Confeccion()
                        v.transaccion_id = c.id
                        v.confeccion_id = asig.id
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dtp = Detalle_produccion()
                                dtp.asignacion_id = asig.id
                                dtp.producto_id = int(i['id'])
                                dtp.cantidad = int(i['cantidad'])
                                dtp.save()
                                dv = Detalle_confeccion()
                                dv.producto_id = dtp.id
                                dv.pvp_by_confec = float(i['pvp'])
                                dv.subtotal = float(i['subtotal'])
                                dv.save()
                        data['id'] = v.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'add_cliente':
                f = ClienteForm(request.POST)
                datos = request.POST
                data = self.save_data(f, datos)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f, datos):
        data = {}
        if f.is_valid():
            if verificar(f.data['cedula']):
                use = User()
                use.username = datos['cedula']
                use.cedula = datos['cedula']
                use.first_name = datos['first_name']
                use.last_name = datos['last_name']
                use.sexo = datos['sexo']
                use.email = datos['email']
                use.telefono = datos['telefono']
                use.celular = datos['celular']
                use.direccion = datos['direccion']
                use.tipo = 0
                use.password = make_password(datos['cedula'])
                use.save()
                data['resp'] = True
                data['cliente'] = use.toJSON()
            else:
                f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                data['error'] = f.errors
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Confeccion'
        data['titulo'] = 'Nueva Confeccion'
        data['nuevo'] = '/confeccion/nuevo'
        data['empresa'] = empresa
        data['form'] = TransaccionForm()
        data['formr'] = ConfeccionForm()
        data['form2'] = Detalle_confeccionform()
        data['detalle'] = []
        data['formc'] = ClienteForm()
        return data


class CrudViewOnline(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Confeccion
    template_name = 'front-end/confeccion/confeccion_online.html'
    permission_required = 'confeccion.add_confeccion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            datos = json.loads(request.POST['confeccion'])
            if action == 'add':
                if datos:
                    with transaction.atomic():
                        us = User.objects.get(id=request.user.id)
                        cli = Cliente.objects.get(cedula=us.cedula)
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = cli.id
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 3
                        c.save()
                        v = Confeccion()
                        v.transaccion_id = c.id
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dv = Detalle_confeccion()
                                dv.confeccion_id = v.id
                                dv.producto_id = int(i['id'])
                                dv.cantidad = int(i['cantidad'])
                                dv.pvp_by_confec = float(i['pvp'])
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
                        us = User.objects.get(id=int(datos['cliente']))
                        cli = Cliente.objects.get(cedula=us.cedula)
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = cli.id
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 3
                        c.save()
                        v = Confeccion()
                        v.transaccion_id = c.id
                        v.estado = 3
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dv = Detalle_confeccion()
                                dv.confeccion_id = v.id
                                dv.producto_id = int(i['id'])
                                dv.cantidad = int(i['cantidad'])
                                dv.pvp_by_confec = float(i['pvp'])
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
        data['titulo'] = 'Nueva Confeccion'
        data['empresa'] = empresa
        data['form'] = TransaccionForm()
        data['form2'] = Detalle_confeccionform()
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
            for i in Detalle_confeccion.objects.filter(confeccion_id=self.kwargs['pk']):
                item = i.confeccion.toJSON()
                item['producto'] = {'producto': i.producto.toJSON()}
                item['pvp'] = format(i.pvp_by_confec, '.2f')
                item['cantidad'] = i.cantidad
                item['subtotal'] = i.subtotal
                data.append(item)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf.html')
            context = {'title': 'Comprobante de Confeccion',
                       'sale': Confeccion.objects.get(pk=self.kwargs['pk']),
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
        return HttpResponseRedirect(reverse_lazy('confeccion:lista'))


class report(ValidatePermissionRequiredMixin, ListView):
    model = Confeccion
    template_name = 'front-end/confeccion/confeccion_report_product.html'
    permission_required = 'confeccion.view_confeccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Confeccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            empresa = Empresa.objects.first()
            iva = empresa.iva/100
            if action == 'report':

                if start_date == '' and end_date == '':
                    confecc = self.model.objects.filter(estado=1)
                    for c in confecc:
                        query = Detalle_confeccion.objects.values('producto__producto_id',
                                                                  'pvp_by_confec').\
                            annotate(Sum('producto__cantidad')).filter(producto__asignacion_id=c.confeccion.id)
                        for p in query:
                            total = p['pvp_by_confec'] * p['producto__cantidad__sum']
                            pr = Producto.objects.get(id=int(p['producto__producto_id']))
                            data.append([
                                    c.transaccion.fecha_trans.strftime("%d/%m/%Y"),
                                    '{}/{}/{}'.format(pr.producto_base.nombre, pr.talla.talla_full(), pr.color.nombre),
                                    int(p['producto__cantidad__sum']),
                                    format(p['pvp_by_confec'], '.2f'),
                                    format(total, '.2f'),
                                    format((float(total) * iva), '.2f'),
                                    format(((float(total) * iva) + float(total)), '.2f')
                                ])
                else:
                    confecc = self.model.objects.filter(estado=1, transaccion__fecha_trans__range=[start_date, end_date])
                    for c in confecc:
                        query = Detalle_confeccion.objects.values('producto__producto_id',
                                                                  'pvp_by_confec'). \
                            annotate(Sum('producto__cantidad')).filter(producto__asignacion_id=c.confeccion.id)
                        for p in query:
                            total = p['pvp_by_confec'] * p['producto__cantidad__sum']
                            pr = Producto.objects.get(id=int(p['producto__producto_id']))
                            data.append([
                                c.transaccion.fecha_trans.strftime("%d/%m/%Y"),
                                '{}/{}/{}'.format(pr.producto_base.nombre, pr.talla.talla_full(), pr.color.nombre),
                                int(p['producto__cantidad__sum']),
                                format(p['pvp_by_confec'], '.2f'),
                                format(total, '.2f'),
                                format((float(total) * iva), '.2f'),
                                format(((float(total) * iva) + float(total)), '.2f')
                            ])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['entidad'] = 'Confeccion de prendas/Por prendas'
        data['titulo'] = 'Reporte de Confeccion de prendas para clientes por prendas'
        data['empresa'] = empresa
        data['year'] = year
        return data


class report_total(ValidatePermissionRequiredMixin, ListView):
    model = Confeccion
    template_name = 'front-end/confeccion/confeccion_report_total.html'
    permission_required = 'confeccion.view_confeccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Confeccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Confeccion.objects.values('transaccion__fecha_trans', 'transaccion__user__first_name',
                                                      'transaccion__user__last_name')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=1)
                else:
                    query = Confeccion.objects.values('transaccion__fecha_trans', 'transaccion__user__first_name',
                                                      'transaccion__user__last_name').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=1). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__user__first_name']+ ' '+ p['transaccion__user__last_name'],
                        format(p['transaccion__subtotal__sum'], '.2f'),
                        format((p['transaccion__iva__sum']), '.2f'),
                        format(p['transaccion__total__sum'], '.2f')
                    ])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Confeccion de prendas para clientes / Entregadas'
        data['titulo'] = 'Reporte de confeccion de prendas para clientes'
        data['empresa'] = empresa
        data['year'] = year
        return data


class report_total_alquilada(ValidatePermissionRequiredMixin, ListView):
    model = Confeccion
    template_name = 'front-end/confeccion/confeccion_report_total_alquiladas.html'
    permission_required = 'confeccion.view_confeccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Confeccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Confeccion.objects.values('transaccion__fecha_trans', 'transaccion__user__first_name',
                                                      'transaccion__user__last_name')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=0)
                else:
                    query = Confeccion.objects.values('transaccion__fecha_trans',
                                                 'transaccion__user__first_name', 'transaccion__user__last_name').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=0). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__user__first_name']+ ' '+ p['transaccion__user__last_name'],
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
        data['entidad'] = 'Confeccion de prendas/Pendientes de entrega'
        data['titulo'] = 'Reporte de Confeccion de prendas/ Pendientes de entrega'
        data['empresa'] = empresa
        data['year'] = year
        return data


class report_total_reservada(ValidatePermissionRequiredMixin, ListView):
    model = Confeccion
    template_name = 'front-end/confeccion/confeccion_report_total_reservadas.html'
    permission_required = 'confeccion.view_confeccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Confeccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Confeccion.objects.values('transaccion__fecha_trans', 'transaccion__user__first_name',
                                                      'transaccion__user__last_name')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=3)
                else:
                    query = Confeccion.objects.values('transaccion__fecha_trans', 'transaccion__user__first_name',
                                                      'transaccion__user__last_name').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=3). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__user__first_name'] + ' ' + p['transaccion__user__last_name'],
                        format(p['transaccion__subtotal__sum'], '.2f'),
                        format((p['transaccion__iva__sum']), '.2f'),
                        format(p['transaccion__total__sum'], '.2f')
                    ])
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Confeccion de prendas para clientes/Reservadas'
        data['titulo'] = 'Reporte de confeccion de prendas para clientes'
        data['empresa'] = empresa
        data['year'] = year
        return data


class report_total_anuladas(ValidatePermissionRequiredMixin, ListView):
    model = Confeccion
    template_name = 'front-end/confeccion/confeccion_report_total_anuladas.html'
    permission_required = 'confeccion.view_confeccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Confeccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Confeccion.objects.values('transaccion__fecha_trans', 'transaccion__user__first_name',
                                                      'transaccion__user__last_name')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=2)
                else:
                    query = Confeccion.objects.values('transaccion__fecha_trans',
                                                 'transaccion__user__first_name', 'transaccion__user__last_name').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=2). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__user__first_name']+ ' '+ p['transaccion__user__last_name'],
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
        data['entidad'] = 'Confeccion de prendas/Anuladas'
        data['titulo'] = 'Reporte de Confeccion de prendas/ Anuladas'
        data['empresa'] = empresa
        data['year'] = year
        return data