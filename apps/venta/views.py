from django.utils.decorators import method_decorator

from apps.cliente.models import Cliente
from apps.compra.models import Compra
from apps.delvoluciones_venta.models import Devolucion
from apps.inventario_productos.models import Inventario_producto
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
# from apps.compra.models import Compra
# from apps.delvoluciones_venta.models import Devolucion
# from apps.inventario.models import Inventario
# from apps.servicio.models import Servicio
# from apps.venta.forms import VentaForm, Detalle_VentaForm
from apps.producto_base.models import Producto_base
from apps.proveedor.forms import ProveedorForm
from apps.transaccion.forms import TransaccionForm
from apps.transaccion.models import Transaccion
from apps.user.forms import UserForm
from apps.user.models import User
from apps.venta.forms import Detalle_VentaForm
from apps.venta.models import Venta, Detalle_venta
from apps.empresa.models import Empresa
from apps.producto.models import Producto

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

opc_icono = 'fa fa-shopping-basket '
opc_entidad = 'Ventas'
crud = '/venta/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/transaccion/transaccion_list.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'venta':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start == '' and end == '':
                    if request.user.tipo == 1:
                        query = Venta.objects.filter(transaccion__tipo=0)
                    else:
                        query = Venta.objects.filter(transaccion__tipo=0, transaccion__user_id=request.user.id)
                else:
                    if request.user.tipo == 1:
                        query = Venta.objects.filter(transaccion__tipo=0, transaccion__fecha_trans__range=[start, end])
                    else:
                        query = Venta.objects.filter(transaccion__tipo=0, transaccion__user_id=request.user.id,
                                                     transaccion__fecha_trans__range=[start, end])
                for c in query:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    result = Detalle_venta.objects.filter(venta_id=id).values('inventario__producto__producto_base_id',
                                                                              'cantidad', 'pvp_actual', 'subtotal'). \
                        annotate(Count('inventario__producto__producto_base_id'))
                    for p in result:
                        pr = Producto_base.objects.get(id=int(p['inventario__producto__producto_base_id']))
                        pb = Producto.objects.get(producto_base_id=pr.id)
                        data.append({
                            'producto': pr.nombre,
                            'categoria': pr.categoria.nombre,
                            'presentacion': pr.presentacion.nombre,
                            'cantidad': p['cantidad'],
                            'pvp': p['pvp_actual'],
                            'subtotal': p['subtotal']
                        })
            elif action == 'estado':
                id = request.POST['id']
                if id:
                    with transaction.atomic():
                        es = Venta.objects.get(id=id)
                        es.estado = 0
                        dev = Devolucion()
                        dev.venta_id = id
                        dev.fecha = datetime.now()
                        dev.save()
                        for i in Detalle_venta.objects.filter(venta_id=id):
                            for a in Inventario_producto.objects.filter(id=i.inventario.id):
                                a.estado = 1
                                a.save()
                        es.save()
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'pagar':
                id = request.POST['id']
                if id:
                    with transaction.atomic():
                        es = Venta.objects.get(id=id)
                        es.estado = 1
                        es.save()
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        if self.request.user.tipo == 0:
            data['entidad'] = 'Compras'
            data['boton'] = 'Nueva Compra'
            data['titulo'] = 'Listado de Compras realizadas'
        else:
            data['entidad'] = opc_entidad
            data['boton'] = 'Nueva Venta'
            data['titulo'] = 'Listado de Ventas'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Venta
    template_name = 'front-end/venta/venta_form.html'
    permission_required = ('venta.add_venta', 'venta.change_venta')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                datos = json.loads(request.POST['ventas'])
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = datos['cliente']
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 0
                        c.save()
                        v = Venta()
                        v.transaccion_id = c.id
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                for in_pr in Inventario_producto.objects.filter(producto_id=i['id'], estado=1)[
                                             :i['cantidad']]:
                                    dv = Detalle_venta()
                                    dv.venta_id = v.id
                                    dv.inventario_id = in_pr.id
                                    dv.cantidad = int(i['cantidad'])
                                    dv.pvp_actual = float(in_pr.producto.pvp)
                                    dv.subtotal = float(i['subtotal'])
                                    in_pr.estado = 0
                                    in_pr.save()
                                    dv.save()
                                stock = Producto_base.objects.get(id=i['producto_base']['id'])
                                stock.stock = int(
                                    Inventario_producto.objects.filter(producto_id=i['id'], estado=1).count())
                                stock.save()
                        data['id'] = v.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'reserva':
                datos = json.loads(request.POST['ventas'])
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = datos['cliente']
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 0
                        c.save()
                        v = Venta()
                        v.transaccion_id = c.id
                        v.estado = 2
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                for in_pr in Inventario_producto.objects.filter(producto_id=i['id'], estado=1)[
                                             :i['cantidad']]:
                                    dv = Detalle_venta()
                                    dv.venta_id = v.id
                                    dv.inventario_id = in_pr.id
                                    dv.cantidad = int(i['cantidad'])
                                    dv.pvp_actual = float(in_pr.producto.pvp)
                                    dv.subtotal = float(i['subtotal'])
                                    in_pr.estado = 0
                                    in_pr.save()
                                    dv.save()
                                stock = Producto_base.objects.get(id=i['producto_base']['id'])
                                stock.stock = int(
                                    Inventario_producto.objects.filter(producto_id=i['id'], estado=1).count())
                                stock.save()
                        data['id'] = v.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Venta'
        data['titulo'] = 'Nueva Venta'
        data['nuevo'] = '/venta/nuevo'
        data['empresa'] = empresa
        data['form'] = TransaccionForm()
        data['form2'] = Detalle_VentaForm()
        data['detalle'] = []
        data['formc'] = UserForm()
        return data


class CrudViewOnline(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Venta
    template_name = 'front-end/venta/venta_form.html'
    permission_required = 'venta.add_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                datos = json.loads(request.POST['ventas'])
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = datos['cliente']
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 0
                        c.save()
                        v = Venta()
                        v.transaccion_id = c.id
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                for in_pr in Inventario_producto.objects.filter(producto_id=i['id'], estado=1)[
                                             :i['cantidad']]:
                                    dv = Detalle_venta()
                                    dv.venta_id = v.id
                                    dv.inventario_id = in_pr.id
                                    dv.cantidad = int(i['cantidad'])
                                    dv.pvp_actual = float(in_pr.producto.pvp)
                                    dv.subtotal = float(i['subtotal'])
                                    in_pr.estado = 0
                                    in_pr.save()
                                    dv.save()
                                stock = Producto_base.objects.get(id=i['producto_base']['id'])
                                stock.stock = int(
                                    Inventario_producto.objects.filter(producto_id=i['id'], estado=1).count())
                                stock.save()
                    data['id'] = v.id
                    data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'reserva':
                datos = json.loads(request.POST['ventas'])
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = datos['cliente']
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 0
                        c.save()
                        v = Venta()
                        v.transaccion_id = c.id
                        v.estado = 2
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                for in_pr in Inventario_producto.objects.filter(producto_id=i['id'], estado=1)[
                                             :i['cantidad']]:
                                    dv = Detalle_venta()
                                    dv.venta_id = v.id
                                    dv.inventario_id = in_pr.id
                                    dv.cantidad = int(i['cantidad'])
                                    dv.pvp_actual = float(in_pr.producto.pvp)
                                    dv.subtotal = float(i['subtotal'])
                                    in_pr.estado = 0
                                    in_pr.save()
                                    dv.save()
                                stock = Producto_base.objects.get(id=i['producto_base']['id'])
                                stock.stock = int(
                                    Inventario_producto.objects.filter(producto_id=i['id'], estado=1).count())
                                stock.save()
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
        data['boton'] = 'Guardar Venta'
        data['titulo'] = 'Nueva Venta'
        data['nuevo'] = '/venta/nuevo'
        data['empresa'] = empresa
        data['form'] = TransaccionForm()
        data['form2'] = Detalle_VentaForm()
        data['detalle'] = []
        data['formc'] = UserForm()
        return data


def CrudView_online(request):
    data = {}
    if request.user.is_authenticated:
        if request.method == 'GET':
            data['icono'] = opc_icono
            data['entidad'] = 'Compras'
            data['boton'] = 'Pagar'
            data['titulo'] = 'Pagar Compra'
            data['nuevo'] = '/'
            data['empresa'] = empresa
            data['form'] = TransaccionForm()
            data['form2'] = Detalle_VentaForm()
            data['detalle'] = []
            user = Cliente.objects.get(cedula=request.user.cedula)
            data['user'] = user
            return render(request, 'front-end/venta/venta_online.html', data)
    else:
        data['key'] = 1
        data['titulo'] = 'Inicio de Sesion'
        data['nomb'] = nombre_empresa()
        return render(request, 'front-end/login.html', data)


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
            result = Detalle_venta.objects.filter(venta_id=self.kwargs['pk']).values(
                'inventario__producto__producto_base_id',
                'cantidad', 'pvp_actual', 'subtotal'). \
                annotate(Count('inventario__producto__producto_base_id'))
            for i in result:
                pr = Producto_base.objects.get(id=int(i['inventario__producto__producto_base_id']))
                pb = Producto.objects.get(producto_base_id=pr.id)
                item = {'producto': {'producto': pb.toJSON()}}
                item['pvp'] = format(i['pvp_actual'], '.2f')
                item['cantidad'] = i['cantidad']
                item['subtotal'] = i['subtotal']
                data.append(item)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf.html')
            context = {'title': 'Comprobante de Venta',
                       'sale': Venta.objects.get(pk=self.kwargs['pk']),
                       'empresa': Empresa.objects.first(),
                       'det_sale': self.pvp_cal(),
                       'icon': 'media/imagen.PNG',
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('venta:lista'))


@csrf_exempt
def grap(request):
    data = {}
    try:
        action = request.POST['action']
        if action == 'chart':
            data = {
                'dat': {
                    'name': 'Total de ventas',
                    'type': 'column',
                    'colorByPoint': True,
                    'showInLegend': True,
                    'data': grap_data(),
                },
                'year': datetime.now().year,
                'chart2': {
                    'data': dataChart2(),
                },
                'chart3': {
                    'compras': datachartcontr(),
                    'ventas': grap_data()
                },
                'tarjets': {
                    'data': data_tarjets()
                }
            }
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


def grap_data():
    year = datetime.now().year
    data = []
    for y in range(1, 13):
        total = Venta.objects.filter(transaccion__fecha_trans__year=year, transaccion__fecha_trans__month=y,
                                     estado=1).aggregate(r=Coalesce(Sum('transaccion__total'), 0)).get('r')
        data.append(float(total))
    return data


def data_tarjets():
    year = datetime.now().year
    ventas = Venta.objects.filter(transaccion__fecha_trans__year=year, estado=1).aggregate(
        r=Coalesce(Count('id'), 0)).get('r')
    compras = Compra.objects.filter(fecha_compra__year=year, estado=1).aggregate(r=Coalesce(Count('id'), 0)).get('r')
    inventario = Inventario_producto.objects.filter(produccion__fecha_ingreso__year=year, estado=1).aggregate(
        r=Coalesce(Count('id'), 0)).get('r')
    agotados = Producto.objects.filter(producto_base__stock__lte=0).count()
    data = {
        'ventas': int(ventas),
        'compras': int(compras),
        'inventario': int(inventario),
        'agotados': int(agotados),
    }
    return data


def dataChart2():
    year = datetime.now().year
    month = datetime.now().month
    data = []
    producto = Producto.objects.all()
    for p in producto:
        total = Detalle_venta.objects.filter(venta__transaccion__fecha_trans__year=year,
                                             venta__transaccion__fecha_trans__month=month,
                                             inventario__producto_id=p).aggregate(
            r=Coalesce(Sum('venta__transaccion__total'), 0)).get('r')
        data.append({
            'name': p.producto_base.nombre,
            'y': float(total)
        })
    return data


def datachartcontr():
    year = datetime.now().year
    data = []
    for y in range(1, 13):
        totalc = Compra.objects.filter(fecha_compra__year=year, fecha_compra__month=y, estado=1).aggregate(
            r=Coalesce(Sum('total'), 0)).get('r')
        data.append(float(totalc))
    return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/venta_report_product.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Detalle_venta.objects.values('venta__transaccion__fecha_trans',
                                                         'inventario__producto__producto_base_id',
                                                         'pvp_actual').order_by().annotate(
                        Sum('cantidad')).filter(venta__estado=1)
                else:
                    query = Detalle_venta.objects.values('venta__transaccion__fecha_trans',
                                                         'inventario__producto__producto_base_id',
                                                         'pvp_actual') \
                        .filter(venta__transaccion__fecha_trans__range=[start_date, end_date],
                                venta__estado=1).order_by().annotate(
                        Sum('cantidad'))
                for p in query:
                    total = p['pvp_actual'] * p['cantidad__sum']
                    print(iva)
                    pr = Producto_base.objects.get(id=int(p['inventario__producto__producto_base_id']))
                    data.append([
                        p['venta__transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        pr.nombre,
                        int(p['cantidad__sum']),
                        format(p['pvp_actual'], '.2f'),
                        format(total, '.2f'),
                        format((float(total) * iva), '.2f'),
                        format(((float(total) * iva) + float(total)), '.2f')
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Ventas'
        data['empresa'] = empresa
        data['filter_prod'] = '/venta/lista'
        return data


class report_total(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/venta_report_total.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Venta.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos', 'transaccion__user__username')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=1)
                else:
                    query = Venta.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
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
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Ventas Finalizadas'
        data['titulo'] = 'Reporte de Ventas'
        data['empresa'] = empresa
        data['filter_prod'] = '/venta/lista'
        return data


class report_total_reserva(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/venta_report_total_reserva.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:

            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Venta.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos', 'transaccion__user__username')\
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=2)
                else:
                    query = Venta.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos',
                                                 'transaccion__user__username').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=2). \
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
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Ventas Reservadas'
        data['titulo'] = 'Reporte de Pedidos'
        data['empresa'] = empresa
        return data
