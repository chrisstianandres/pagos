from django.utils.decorators import method_decorator

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
# from apps.compra.models import Compra
# from apps.delvoluciones_venta.models import Devolucion
# from apps.inventario.models import Inventario
# from apps.servicio.models import Servicio
from apps.reparacion.forms import ReparacionForm, Detalle_reparacionform
from apps.reparacion.models import Reparacion, Detalle_reparacion
from apps.empresa.models import Empresa
from apps.producto.models import Producto

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from apps.transaccion.forms import TransaccionForm
from apps.transaccion.models import Transaccion

opc_icono = 'fas fa-tools'
opc_entidad = 'Reparaciones'
crud = '/reparacion/crear'
empresa = nombre_empresa()

#
# class lista(ValidatePermissionRequiredMixin, ListView):
#     model = Producto
#     template_name = 'front-end/reparacion/reparacion_list.html'
#     permission_required = 'reparacion.view_reparacion'
#
#     @csrf_exempt
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             start = request.POST['start_date']
#             end = request.POST['end_date']
#             if action == 'reparacion':
#                 data = []
#                 if start == '' and end == '':
#                     query = Transaccion.objects.filter(tipo=1)
#                 else:
#                     query = Transaccion.objects.filter(tipo=1, fecha_trans__range=[start, end])
#                 for c in query:
#                     data.append(c.toJSON())
#             else:
#                 data['error'] = 'No ha seleccionado una opcion'
#         except Exception as e:
#             data['error'] = 'No ha seleccionado una opcion'
#         return JsonResponse(data, safe=False)
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['icono'] = opc_icono
#         data['entidad'] = opc_entidad
#         data['boton'] = 'Nueva Reparacion'
#         data['titulo'] = 'Listado de Reparaciones'
#         data['nuevo'] = '/Reparacion/nuevo'
#         data['empresa'] = empresa
#         return data


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


# @csrf_exempt
# def data(request):
#     data = []
#     start_date = request.POST.get('start_date', '')
#     end_date = request.POST.get('end_date', '')
#     try:
#         if start_date == '' and end_date == '':
#             venta = Venta.objects.all()
#         else:
#             venta = Venta.objects.filter(fecha_venta__range=[start_date, end_date])
#         for c in venta:
#             data.append([
#                 c.fecha_venta.strftime('%d-%m-%Y'),
#                 c.cliente.nombres + " " + c.cliente.apellidos,
#                 c.empleado.get_full_name(),
#                 format(c.total, '.2f'),
#                 c.id,
#                 c.get_estado_display(),
#                 c.id
#             ])
#
#     except:
#         pass
#     return JsonResponse(data, safe=False)
#
#
# def nuevo(request):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../venta/get_producto',
#         'crudserv': '../venta/get_servicio',
#         'empresa': empresa,
#         'boton': 'Guardar Venta', 'action': 'add', 'titulo': 'Nuevo Registro de una Venta',
#         'key': ''
#     }
#     if request.method == 'GET':
#         data['form'] = VentaForm()
#         data['form2'] = Detalle_VentaForm()
#         data['formc'] = ClienteForm()
#         data['detalle'] = []
#     return render(request, 'front-end/venta/venta_form.html', data)
#
#
# @csrf_exempt
# def crear(request):
#     data = {}
#     if request.method == 'POST':
#         datos = json.loads(request.POST['ventas'])
#         if datos:
#             dtp = []
#             with transaction.atomic():
#                 c = Venta()
#                 c.fecha_venta = datos['fecha_venta']
#                 c.cliente_id = datos['cliente']
#                 c.empleado_id = request.user.id
#                 c.subtotal = float(datos['subtotal'])
#                 c.iva = float(datos['iva'])
#                 c.total = float(datos['total'])
#                 c.save()
#                 if datos['productos'] and datos['servicios']:
#                     for i in datos['productos']:
#                         dv = Detalle_venta()
#                         dv.venta_id = c.id
#                         dv.producto_id = i['producto']['id']
#                         dv.cantidadp = int(i['cantidad'])
#                         x = Producto.objects.get(pk=i['producto']['id'])
#                         dv.pvp_actual = float(x.pvp)
#                         x.stock = x.stock - int(i['cantidad'])
#                         dv.subtotalp = float(i['subtotal'])
#                         x.save()
#                         inv = Inventario.objects.filter(producto_id=i['producto']['id'], estado=1)[:i['cantidad']]
#                         for itr in inv:
#                             x = Inventario.objects.get(pk=itr.id)
#                             x.estado = 0
#                             x.venta_id = c.id
#                             x.save()
#                         for s in datos['servicios']:
#                             dv.servicio_id = s['id']
#                             dv.cantidads = int(s['cantidad'])
#                             dv.subtotals = float(s['subtotal'])
#                             dv.pvp_actual_s = float(s['pvp'])
#                             dv.save()
#                         data['id'] = c.id
#                         data['resp'] = True
#                 elif datos['productos']:
#                     for i in datos['productos']:
#                         dv = Detalle_venta()
#                         dv.venta_id = c.id
#                         dv.producto_id = i['producto']['id']
#                         dv.cantidadp = int(i['cantidad'])
#                         dv.subtotalp = float(i['subtotal'])
#                         x = Producto.objects.get(pk=i['producto']['id'])
#                         dv.pvp_actual = float(x.pvp)
#                         x.stock = x.stock - int(i['cantidad'])
#                         x.save()
#                         inv = Inventario.objects.filter(producto_id=i['producto']['id'], estado=1)[:i['cantidad']]
#                         for itr in inv:
#                             x = Inventario.objects.get(pk=itr.id)
#                             x.estado = 0
#                             x.venta_id = c.id
#                             x.save()
#                             dv.save()
#                     data['id'] = c.id
#                     data['resp'] = True
#                 else:
#                     for i in datos['servicios']:
#                         dv = Detalle_venta()
#                         dv.venta_id = c.id
#                         dv.servicio_id = i['id']
#                         dv.cantidads = int(i['cantidad'])
#                         dv.subtotals = float(i['subtotal'])
#                         dv.pvp_actual_s = float(i['pvp'])
#                         dv.save()
#                     data['id'] = c.id
#                     data['resp'] = True
#         else:
#             data['resp'] = False
#             data['error'] = "Datos Incompletos"
#     return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# def editar(request, id):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../../venta/get_producto', 'empresa': empresa,
#         'boton': 'Editar Venta', 'action': 'edit', 'titulo': 'Editar Registro de una Venta',
#         'key': id
#     }
#     venta = Venta.objects.get(id=id)
#     if request.method == 'GET':
#         data['form'] = VentaForm(instance=venta)
#         data['form2'] = Detalle_VentaForm()
#         data['detalle'] = json.dumps(get_detalle_productos(id))
#     return render(request, 'front-end/venta/venta_form.html', data)
#
#
# @csrf_exempt
# def editar_save(request):
#     data = {}
#     datos = json.loads(request.POST['ventas'])
#     if request.POST['action'] == 'edit':
#
#         with transaction.atomic():
#             # c = Compra.objects.get(pk=self.get_object().id)
#             c = Venta.objects.get(pk=request.POST['key'])
#             c.fecha_venta = datos['fecha_venta']
#             c.cliente_id = datos['cliente']
#             c.subtotal = float(datos['subtotal'])
#             c.iva = float(datos['iva'])
#             c.total = float(datos['total'])
#             c.save()
#             c.detalle_venta_set.all().delete()
#             for i in datos['productos']:
#                 dv = Detalle_venta()
#                 dv.venta_id = c.id
#                 dv.producto_id = i['id']
#                 dv.cantidad = int(i['cantidad'])
#                 dv.save()
#                 data['resp'] = True
#     else:
#         data['resp'] = False
#         data['error'] = "Datos Incompletos"
#     return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# def get_detalle_productos(id):
#     data = []
#     try:
#         for i in Detalle_venta.objects.filter(venta_id=id):
#             iva_emp = Empresa.objects.get(pk=1)
#             item = i.producto.toJSON()
#             item['cantidad'] = i.cantidad
#             item['iva_emp'] = format(iva_emp.iva, '.2f')
#             data.append(item)
#     except:
#         pass
#     return data
#
#
# @csrf_exempt
# def get_producto(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             query = Inventario.objects.filter(producto_id=id, estado=1, select=0)[0:1]
#             iva_emp = Empresa.objects.get(pk=1)
#             data = []
#             for i in query:
#                 item = i.toJSON()
#                 item['producto'] = i.producto.toJSON()
#                 item['pvp'] = (i.producto.pvp * 100) / (iva_emp.iva + 100)
#                 item['cantidad'] = 1
#                 item['subtotal'] = 0.00
#                 item['iva_emp'] = iva_emp.iva / 100
#                 data.append(item)
#                 i.select = 1
#                 i.save()
#         else:
#             data['error'] = 'No ha selecionado ningun Producto'
#     except Exception as e:
#         data['error'] = 'Ha ocurrido un error'
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def get_servicio(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             servicio = Servicio.objects.filter(pk=id)
#             iva_emp = Empresa.objects.get(pk=1)
#             data = []
#             for i in servicio:
#                 item = i.toJSON()
#                 item['pvp'] = 1.00
#                 item['cantidad'] = 1
#                 item['subtotal'] = 0.00
#                 item['iva_emp'] = iva_emp.iva / 100
#                 data.append(item)
#         else:
#             data['error'] = 'No ha selecionado ningun Servicio'
#     except Exception as e:
#         data['error'] = 'Ha ocurrido un error'
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def get_detalle(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             data = []
#             result = Detalle_venta.objects.filter(venta_id=id)
#             empresa = Empresa.objects.get(pk=1)
#             for p in result:
#                 if p.producto != None:
#                     data.append({
#                         'producto': p.producto.nombre,
#                         'categoria': p.producto.categoria.nombre,
#                         'presentacion': p.producto.presentacion.nombre,
#                         'cantidad': p.cantidadp,
#                         'pvp': (p.pvp_actual * 100) / (empresa.iva + 100),
#                         'subtotal': p.subtotalp
#                     })
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def get_detalle_serv(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             data = []
#             result = Detalle_venta.objects.filter(venta_id=id)
#             for p in result:
#                 if p.servicio != None:
#                     data.append({
#                         'servicio': p.servicio.nombre,
#                         'cantidad': p.cantidads,
#                         'pvp': (p.pvp_actual_s),
#                         'subtotal': p.subtotals
#                     })
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def estado(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             with transaction.atomic():
#                 es = Venta.objects.get(id=id)
#                 es.estado = 0
#                 dev = Devolucion()
#                 dev.venta_id = id
#                 dev.fecha = datetime.now()
#                 dev.save()
#                 for i in Detalle_venta.objects.filter(venta_id=id):
#                     if i.producto==None:
#                         es.save()
#                     else:
#                         ch = Producto.objects.get(id=i.producto.id)
#                         ch.stock = int(ch.stock) + int(i.cantidadp)
#                         ch.save()
#                         for a in Inventario.objects.filter(venta_id=id):
#                             a.estado = 1
#                             a.select = 0
#                             a.venta_id = None
#                             a.save()
#                             es.save()
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data)
#
#
# @csrf_exempt
# def eliminar(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             es = Venta.objects.get(id=id)
#             es.delete()
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data)
#
#
# @csrf_exempt
# def grap(request):
#     data = {}
#     try:
#         action = request.POST['action']
#         if action == 'chart':
#             data = {
#                 'dat': {
#                     'name': 'Total de ventas',
#                     'type': 'column',
#                     'colorByPoint': True,
#                     'showInLegend': True,
#                     'data': grap_data(),
#                 },
#                 'year': datetime.now().year,
#                 'chart2': {
#                     'data': dataChart2(),
#                 },
#                 'chart3': {
#                     'compras': datachartcontr(),
#                     'ventas': grap_data()
#                 },
#                 'tarjets': {
#                     'data': data_tarjets()
#                 }
#             }
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)
#
#
# def grap_data():
#     year = datetime.now().year
#     data = []
#     for y in range(1, 13):
#         total = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month=y, estado=1).aggregate(
#             r=Coalesce(Sum('total'), 0)).get('r')
#         data.append(float(total))
#     return data
#
#
# def data_tarjets():
#     year = datetime.now().year
#     ventas = Venta.objects.filter(fecha_venta__year=year, estado=1).aggregate(r=Coalesce(Count('id'), 0)).get('r')
#     compras = Compra.objects.filter(fecha_compra__year=year, estado=1).aggregate(r=Coalesce(Count('id'), 0)).get('r')
#     inventario = Inventario.objects.filter(compra__fecha_compra__year=year, estado=1).aggregate(
#         r=Coalesce(Count('id'), 0)).get('r')
#     data = {
#         'ventas': int(ventas),
#         'compras': int(compras),
#         'inventario': int(inventario),
#     }
#     return data
#
#
# def dataChart2():
#     year = datetime.now().year
#     month = datetime.now().month
#     data = []
#     producto = Producto.objects.all()
#     for p in producto:
#         total = Detalle_venta.objects.filter(venta__fecha_venta__year=year, venta__fecha_venta__month=month,
#                                              producto_id=p).aggregate(r=Coalesce(Sum('venta__total'), 0)).get('r')
#         data.append({
#             'name': p.nombre,
#             'y': float(total)
#         })
#     return data
#
#
# def datachartcontr():
#     year = datetime.now().year
#     data = []
#     for y in range(1, 13):
#         totalc = Compra.objects.filter(fecha_compra__year=year, fecha_compra__month=y, estado=1).aggregate(
#             r=Coalesce(Sum('total'), 0)).get('r')
#         data.append(float(totalc))
#     return data
#
#
# class printpdf(View):
#
#     def link_callback(self, uri, rel):
#         """
#         Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#         resources
#         """
#         result = finders.find(uri)
#         if result:
#             if not isinstance(result, (list, tuple)):
#                 result = [result]
#             result = list(os.path.realpath(path) for path in result)
#             path = result[0]
#         else:
#             sUrl = settings.STATIC_URL  # Typically /static/
#             sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
#             mUrl = settings.MEDIA_URL  # Typically /media/
#             mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/
#
#             if uri.startswith(mUrl):
#                 path = os.path.join(mRoot, uri.replace(mUrl, ""))
#             elif uri.startswith(sUrl):
#                 path = os.path.join(sRoot, uri.replace(sUrl, ""))
#             else:
#                 return uri
#
#         # make sure that file exists
#         if not os.path.isfile(path):
#             raise Exception(
#                 'media URI must start with %s or %s' % (sUrl, mUrl)
#             )
#         return path
#
#     def pvp_cal(self, *args, **kwargs):
#         data = []
#         try:
#             iva_emp = Empresa.objects.get(pk=1)
#             for i in Detalle_venta.objects.filter(venta_id=self.kwargs['pk']):
#                 item = i.venta.toJSON()
#                 item['producto'] = i.producto.toJSON()
#                 item['servicio'] = i.servicio.toJSON()
#                 item['pvp'] = format(((i.pvp_actual * 100) / (iva_emp.iva + 100)), '.2f')
#                 item['pvp_s'] = format(((i.pvp_actual_s * 100) / (iva_emp.iva + 100)), '.2f')
#                 item['cantidadp'] = i.cantidadp
#                 item['subtotalp'] = i.subtotalp
#                 item['cantidads'] = i.cantidads
#                 item['subtotals'] = i.subtotals
#                 data.append(item)
#         except:
#             pass
#         return data
#
#     def get(self, request, *args, **kwargs):
#         try:
#             template = get_template('front-end/report/pdf.html')
#             context = {'title': 'Comprobante de Venta',
#                        'sale': Venta.objects.get(pk=self.kwargs['pk']),
#                        'det_sale': self.pvp_cal(),
#                        'empresa': Empresa.objects.get(id=1),
#                        'icon': 'media/logo_don_chuta.png',
#                        'inventario': Inventario.objects.filter(venta_id=self.kwargs['pk'])
#                        }
#             html = template.render(context)
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#             pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
#             return response
#         except:
#             pass
#         return HttpResponseRedirect(reverse_lazy('venta:lista'))
#
#
# @csrf_exempt
# def data_report(request):
#     data = []
#     start_date = request.POST.get('start_date', '')
#     end_date = request.POST.get('end_date', '')
#     tipo = request.POST.get('tipo', '')
#     empresa = Empresa.objects.get(pk=1)
#     iva = float(empresa.iva / 100)
#     try:
#         if int(tipo) == 1:
#             if start_date == '' and end_date == '':
#                 query = Detalle_venta.objects.exclude(cantidadp=0).values('venta__fecha_venta', 'producto__nombre',
#                                                                           'pvp_actual').order_by().annotate(
#                     Sum('cantidadp')).filter(venta__estado=1)
#             else:
#                 query = Detalle_venta.objects.exclude(cantidadp=0).values('venta__fecha_venta', 'producto__nombre',
#                                                                           'pvp_actual') \
#                     .filter(venta__fecha_venta__range=[start_date, end_date], venta__estado=1).order_by().annotate(
#                     Sum('cantidadp'))
#             for p in query:
#                 total = p['pvp_actual'] * p['cantidadp__sum']
#                 total_sin_iva = float((total * 100) / (100 + empresa.iva))
#                 data.append([
#                     p['venta__fecha_venta'].strftime("%d/%m/%Y"),
#                     p['producto__nombre'],
#                     'Producto',
#                     int(p['cantidadp__sum']),
#                     format(p['pvp_actual'], '.2f'),
#                     format(total_sin_iva, '.2f'),
#                     format(total_sin_iva * iva, '.2f'),
#                     format(total, '.2f')
#                 ])
#         elif int(tipo) == 2:
#             if start_date == '' and end_date == '':
#                 query = Detalle_venta.objects.exclude(cantidads=0).values('venta__fecha_venta', 'servicio__nombre',
#                                                                           'pvp_actual_s').annotate(
#                     Sum('cantidads')).filter(venta__estado=1)
#             else:
#                 query = Detalle_venta.objects.exclude(cantidads=0).values('venta__fecha_venta', 'servicio__nombre',
#                                                                           'pvp_actual_s') \
#                     .filter(venta__fecha_venta__range=[start_date, end_date], venta__estado=1).annotate(
#                     Sum('cantidads'))
#             for p in query:
#                 total = float(p['pvp_actual_s'] * p['cantidads__sum'])
#                 data.append([
#                     p['venta__fecha_venta'].strftime("%d/%m/%Y"),
#                     p['servicio__nombre'],
#                     'Servicio',
#                     int(p['cantidads__sum']),
#                     format(p['pvp_actual_s'], '.2f'),
#                     format(total, '.2f'),
#                     format(total * iva, '.2f'),
#                     format(total * (1 + iva), '.2f')
#                 ])
#         else:
#             if start_date == '' and end_date == '':
#                 query = Detalle_venta.objects.exclude(cantidadp=0).values('venta__fecha_venta', 'producto__nombre',
#                                                                           'pvp_actual').order_by().annotate(
#                     Sum('cantidadp')).filter(venta__estado=1)
#                 query2 = Detalle_venta.objects.exclude(cantidads=0).values('venta__fecha_venta', 'servicio__nombre',
#                                                                            'pvp_actual_s').annotate(
#                     Sum('cantidads')).filter(venta__estado=1)
#             else:
#                 query = Detalle_venta.objects.exclude(cantidadp=0).values('venta__fecha_venta', 'producto__nombre',
#                                                                           'pvp_actual') \
#                     .filter(venta__fecha_venta__range=[start_date, end_date], venta__estado=1).order_by().annotate(
#                     Sum('cantidadp'))
#                 query2 = Detalle_venta.objects.exclude(cantidads=0).values('venta__fecha_venta', 'servicio__nombre',
#                                                                            'pvp_actual_s') \
#                     .filter(venta__fecha_venta__range=[start_date, end_date], venta__estado=1).annotate(
#                     Sum('cantidads'))
#             for p in query:
#                 totalp = p['pvp_actual'] * p['cantidadp__sum']
#                 total_sin_iva = float((totalp * 100) / (100 + empresa.iva))
#                 data.append([
#                     p['venta__fecha_venta'].strftime("%d/%m/%Y"),
#                     p['producto__nombre'],
#                     'Producto',
#                     int(p['cantidadp__sum']),
#                     format(p['pvp_actual'], '.2f'),
#                     format(total_sin_iva, '.2f'),
#                     format(total_sin_iva * iva, '.2f'),
#                     format(totalp, '.2f')
#                 ])
#
#             for q in query2:
#                 totals = float(q['pvp_actual_s'] * q['cantidads__sum'])
#                 data.append([
#                     q['venta__fecha_venta'].strftime("%d/%m/%Y"),
#                     q['servicio__nombre'],
#                     'Servicio',
#                     int(q['cantidads__sum']),
#                     format(q['pvp_actual_s'], '.2f'),
#                     format(totals, '.2f'),
#                     format(totals * iva, '.2f'),
#                     format(totals * (1 + iva), '.2f')
#                 ])
#     except:
#         pass
#     return JsonResponse(data, safe=False)
#
#
# class report(ListView):
#     model = Venta
#     template_name = 'front-end/venta/venta_report_product.html'
#
#     def get_queryset(self):
#         return Venta.objects.none()
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['icono'] = opc_icono
#         data['entidad'] = opc_entidad
#         data['boton'] = 'Nueva Venta'
#         data['titulo'] = 'Listado de Ventas'
#         data['nuevo'] = '/venta/nuevo'
#         data['empresa'] = empresa
#         data['filter_prod'] = '/venta/lista'
#         return data
#
#
# @csrf_exempt
# def data_report_total(request):
#     x = Venta.objects.get(id=35)
#     x.iva = float(1.80)
#     x.save()
#     data = []
#     start_date = request.POST.get('start_date', '')
#     end_date = request.POST.get('end_date', '')
#     try:
#         if start_date == '' and end_date == '':
#             query = Venta.objects.values('fecha_venta', 'cliente__nombres', 'cliente__apellidos', 'empleado__first_name'
#                                          , 'empleado__last_name').annotate(Sum('subtotal')). \
#                 annotate(Sum('iva')).annotate(Sum('total')).filter(estado=1)
#         else:
#             query = Venta.objects.values('fecha_venta', 'cliente__nombres', 'cliente__apellidos',
#                                          'empleado__first_name',
#                                          'empleado__last_name').filter(
#                 fecha_venta__range=[start_date, end_date], estado=1).annotate(Sum('subtotal')). \
#                 annotate(Sum('iva')).annotate(Sum('total'))
#         for p in query:
#             data.append([
#                 p['fecha_venta'].strftime("%d/%m/%Y"),
#                 p['cliente__nombres'] + " " + p['cliente__apellidos'],
#                 p['empleado__first_name'] + " " + p['empleado__last_name'],
#                 format(p['subtotal__sum'], '.2f'),
#                 format((p['iva__sum']), '.2f'),
#                 format(p['total__sum'], '.2f')
#             ])
#     except:
#         pass
#     return JsonResponse(data, safe=False)
#
#
# class report_total(ListView):
#     model = Venta
#     template_name = 'front-end/venta/venta_report_total.html'
#
#     def get_queryset(self):
#         return Venta.objects.none()
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['icono'] = opc_icono
#         data['entidad'] = opc_entidad
#         data['boton'] = 'Nueva Venta'
#         data['titulo'] = 'Listado de Ventas'
#         data['nuevo'] = '/venta/nuevo'
#         data['empresa'] = empresa
#         data['filter_prod'] = '/venta/lista'
#         return data
