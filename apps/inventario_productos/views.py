import json

from django.db import transaction
from django.db.models import Q, Max
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from apps.backEnd import nombre_empresa
from apps.inventario_productos.models import Inventario_producto

from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.models import Producto

opc_icono = 'fas fa-warehouse'
opc_entidad = 'Inventario'
crud = '/inventario/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Inventario_producto
    template_name = 'front-end/inventario/inventario_list.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Inventario_producto.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                venta = ''
                estado = ''
                if start_date == '' and end_date == '':
                    compra = Inventario_producto.objects.all()
                else:
                    compra = Inventario_producto.objects.filter(Q(compra__fecha_compra__range=[start_date, end_date]) |
                                                       Q(venta__fecha_venta__range=[start_date, end_date]))
                for c in compra:
                    data.append([
                        c.id,
                        c.producto.nombre,
                        c.producto.categoria.nombre,
                        c.producto.presentacion.nombre,
                        estado
                    ])
            elif action == 'search':
                data = []
                query = Inventario_producto.objects.values('producto_id', 'producto__producto_base__nombre').\
                    filter(estado=1).order_by().annotate(Max('producto__id'))
                for p in query:
                    result = {
                        'id': int(p['producto_id']),
                        'text': str(p['producto__producto_base__nombre'])
                    }
                    data.append(result)
                    print(data)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte  de Inventario'
        data['empresa'] = empresa
        return data


# @csrf_exempt
# def data(request):
#     data = []
#     start_date = request.POST.get('start_date', '')
#     end_date = request.POST.get('end_date', '')
#     venta = ''
#     estado = ''
#     try:
#         if start_date == '' and end_date == '':
#             compra = Inventario.objects.all()
#             for c in compra:
#                 if c.venta == None:
#                     venta = 'No vendido'
#                     estado = 'En Stock'
#                 else:
#                     venta = c.venta.fecha_venta
#                     estado = 'Vendido'
#                 data.append([
#                     c.id,
#                     c.compra.fecha_compra.strftime('%d-%m-%Y'),
#                     venta,
#                     c.producto.nombre,
#                     c.producto.categoria.nombre,
#                     c.producto.presentacion.nombre,
#                     c.serie,
#                     estado
#                 ])
#         else:
#             compra = Inventario.objects.filter(Q(compra__fecha_compra__range=[start_date, end_date]) |
#                                                Q(venta__fecha_venta__range=[start_date, end_date]))
#             for c in compra:
#                 if c.venta == None:
#                     venta = 'No vendido'
#                     estado = 'En Stock'
#                 else:
#                     venta = c.venta.fecha_venta
#                     estado = 'Vendido'
#                 data.append([
#                     c.id,
#                     c.compra.fecha_compra.strftime('%d-%m-%Y'),
#                     venta,
#                     c.producto.nombre,
#                     c.producto.categoria.nombre,
#                     c.producto.presentacion.nombre,
#                     c.serie,
#                     estado,
#                     c.id
#                 ])
#     except:
#         pass
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def nuevo(request):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
#         'boton': 'Guardar Inventario', 'action': 'add', 'titulo': 'Nuevo Registro de un Inventario',
#     }
#     if request.method == 'POST':
#         # inputs = request.POST.getlist('datos')
#         datos = json.loads(request.POST['datos'])
#         data['list'] = datos
#
#     return render(request, 'front-end/inventario/inventario_form.html', data)
#
#
# @csrf_exempt
# def crear(request):
#     data = {}
#     if request.method == 'POST':
#         datos = json.loads(request.POST['inventario'])
#         if datos:
#             with transaction.atomic():
#                 p = []
#                 for i in datos['prod']:
#                     if i['serie'] == 0:
#                         data['resp'] = False
#                         data['error'] = "Datos Incompletos"
#                     else:
#                         x = i['producto']
#                         x['compra'] = i['id']
#                         x['serie'] = i['serie']
#                         p.append(x)
#                 for a in p:
#                     dv = Inventario()
#                     dv.compra_id = int(a['compra'])
#                     dv.producto_id = a['id']
#                     dv.serie = str(a['serie'])
#                     dv.save()
#                     data['resp'] = True
#     return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# @csrf_exempt
# def eliminar(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             ps = Inventario.objects.get(pk=id)
#             ps.delete()
#             x = Producto.objects.get(pk=ps.producto.id)
#             x.stock = x.stock - 1
#             x.save()
#             data['resp'] = True
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = 'No se puede eliminar este cliente porque esta referenciado en otros procesos'
#         data['content'] = 'Intenta con otro cliente'
#     return JsonResponse(data)
#
#
# @csrf_exempt
# def data_select(request):
#     data = {}
#     try:
#         query = Inventario.objects.values('producto_id', 'producto__nombre').filter(estado=1, select=0).order_by(). \
#             annotate(Max('producto__id'))
#         print(Inventario.objects.values('producto_id', 'producto__nombre'))
#         data = []
#         for p in query:
#             result = {
#                 'id': int(p['producto_id']),
#                 'text': str(p['producto__nombre'])
#             }
#             data.append(result)
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def remove_select(request):
#     data = {}
#     try:
#         id = json.loads(request.POST['productos'])
#         pik = json.loads(request.POST['id'])
#         key = json.loads(request.POST['key'])
#         if key == 1:
#             if id:
#                 for p in id:
#                     ps = Inventario.objects.get(pk=int(p['id']))
#                     ps.select = 0
#                     ps.save()
#                     data['resp'] = True
#         elif pik:
#             ps = Inventario.objects.get(pk=pik)
#             ps.select = 0
#             ps.save()
#             data['resp'] = True
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data)
#
#
# @csrf_exempt
# def check_product(request):
#     data = {}
#     try:
#         producto = Inventario.objects.filter(venta=None)
#         for p in producto:
#             if p.select == 1:
#                 c = Inventario.objects.get(pk=p.id)
#                 c.select = 0
#                 c.save()
#                 x = Producto.objects.get(pk=2)
#                 x.stock=0
#                 x.save()
#                 x = Producto.objects.get(pk=3)
#                 x.stock = 0
#                 x.save()
#
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=True)
