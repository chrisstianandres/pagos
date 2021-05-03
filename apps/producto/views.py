import json

from datetime import datetime, timedelta
from django.db.models import Q, Sum, Max
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.categoria.forms import CategoriaForm
from apps.color.forms import ColorForm
from apps.empresa.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.forms import ProductoForm, Producto_baseForm
from apps.producto.models import Producto
from apps.producto_base.models import Producto_base
from apps.talla.forms import TallaForm
from apps.venta.models import Detalle_venta

opc_icono = 'fa fa-tshirt'
opc_entidad = 'Prendas de Vestir'
crud = '/producto/nuevo'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'front-end/producto/producto_list.html'
    permission_required = 'producto.view_producto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Producto.objects.all():
                    data.append(c.toJSON())
            elif action == 'list_add':
                data = []
                for c in Producto_base.objects.filter(tipo=0):
                    data.append(c.toJSON())
            elif action == 'list_venta':
                data = []
                vent = Producto.objects.filter(stock__gte=1)
                ids = json.loads(request.POST['ids'])
                for c in vent.exclude(id__in=ids):
                    data.append(c.toJSON())
            elif action == 'search':
                data = []
                term = request.POST['term']
                ids = json.loads(request.POST['ids'])
                query = Producto.objects.filter(producto_base__nombre__icontains=term, stock__gte=1)
                for a in query.exclude(id__in=ids)[0:10]:
                    result = {'id': int(a.id), 'text': str(str(a.producto_base.nombre) + ' / ' + str(a.color.nombre) + ' / ' + str(
                                  a.talla.talla_full()))}
                    data.append(result)
            elif action == 'search_rep':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                query = Producto.objects.filter(
                    Q(producto_base__nombre__icontains=term) | Q(color__nombre__icontains=term))
                for a in query.exclude(id__in=ids)[0:10]:
                    result = {'id': int(a.id),
                              'text': str(str(a.producto_base.nombre) + ' / ' + str(a.color.nombre) + ' / ' + str(
                                  a.talla.talla_full()))}
                    data.append(result)
            elif action == 'lista_reparacion':
                data = []
                vent = Producto.objects.all()
                ids = json.loads(request.POST['ids'])
                for c in vent.exclude(id__in=ids):
                    data.append(c.toJSON())
            elif action == 'search_asig_table':
                data = []
                ids = json.loads(request.POST['ids'])
                query = Producto.objects.all()
                for a in query.exclude(id__in=ids):
                    data.append(a.toJSON())
            elif action == 'get':
                data = []
                id = request.POST['id']
                producto = Producto.objects.filter(pk=id)
                empresa = Empresa.objects.first()
                for i in producto:
                    item = i.toJSON()
                    item['cantidad'] = 5
                    item['cantidad_venta'] = 1
                    item['subtotal'] = 0.00
                    item['iva_emp'] = empresa.iva
                    data.append(item)
            elif action == 'get_rep':
                data = []
                id = request.POST['id']
                producto = Producto.objects.filter(pk=id)
                empresa = Empresa.objects.first()
                for i in producto:
                    item = i.toJSON()
                    item['cantidad'] = 1
                    item['pvp'] = 1.00
                    item['subtotal'] = 0.00
                    item['iva_emp'] = empresa.iva
                    data.append(item)
            elif action == 'get_confec':
                data = []
                id = request.POST['id']
                producto = Producto.objects.filter(pk=id)
                empresa = Empresa.objects.first()
                for i in producto:
                    item = i.toJSON()
                    item['cantidad'] = 1
                    item['pvp'] = format(i.pvp_confec, '.2f')
                    item['subtotal'] = 0.00
                    item['iva_emp'] = empresa.iva
                    data.append(item)
            elif action == 'sitio':
                data = []
                h = datetime.today()
                query = Detalle_venta.objects.filter(venta__transaccion__fecha_trans__month=h.month,
                                                     venta__estado=1).values('inventario__producto__producto_base_id',
                                                                             'inventario__producto_id',
                                                                             'inventario__producto__pvp',
                                                                             'inventario__producto__pvp_alq',
                                                                             'inventario__producto__pvp_confec',
                                                                             'inventario__producto__imagen').annotate(
                    total=Sum('cantidad')).order_by('-total')[0:3]
                for i in query:
                    px = Producto_base.objects.get(id=int(i['inventario__producto__producto_base_id']))
                    pr = Producto.objects.get(id=int(i['inventario__producto_id']))
                    item = {'info': px.nombre, 'descripcion': px.descripcion}
                    item['id_venta'] = int(i['inventario__producto_id'])
                    item['id_reparacion'] = int(pr.id)
                    item['id_confeccion'] = int(pr.id)
                    item['pvp'] = format(i['inventario__producto__pvp'], '.2f')
                    item['pvp_alq'] = format(i['inventario__producto__pvp_alq'], '.2f')
                    item['pvp_confec'] = format(i['inventario__producto__pvp_confec'], '.2f')
                    item['imagen'] = pr.get_image()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Producto'
        data['titulo'] = 'Listado de Productos'
        data['nuevo'] = '/producto/nuevo'
        data['empresa'] = empresa
        return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'front-end/producto/producto_report.html'
    permission_required = 'producto.view_producto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                data = []
                for c in Producto.objects.all():
                    data.append(c.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Producto'
        data['titulo'] = 'Listado de Productos'
        data['nuevo'] = '/producto/nuevo'
        data['empresa'] = empresa
        return data


class sitio(ListView):
    model = Producto

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'categoria':
                data = []
                id = request.POST['id']
                if id == '0':
                    query = Producto.objects.all()
                else:
                    query = Producto.objects.filter(producto_base__categoria_id=id)
                for i in query:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Producto'
        data['titulo'] = 'Listado de Productos'
        data['nuevo'] = '/producto/nuevo'
        data['empresa'] = empresa
        return data


class Createview(ValidatePermissionRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = 'producto:lista'
    template_name = 'front-end/producto/producto_form.html'
    permission_required = 'producto.add_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = self.form_class(request.POST or None, request.FILES or None)
                if f.is_valid():
                    if Producto.objects.filter(producto_base_id=f.data['producto_base'], color_id=f.data['color'],
                                               talla_id=f.data['talla']):
                        f.add_error("producto_base", "Prenda de vestir repetida")
                        data['error'] = f.errors
                    else:
                        f.save()
                        data['resp'] = True
                else:
                    data['error'] = f.errors
                    data['form'] = f
            elif action == 'delete':
                pk = request.POST['id']
                f = Producto.objects.get(pk=pk)
                f.delete()
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Producto_base.objects.filter(nombre__icontains=term)[0:10]
                for a in query:
                    result = {'id': int(a.id),
                              'text': 'Nombre: ' + str(a.nombre) + ' / ' + 'Descripcion: ' + str(a.descripcion)}
                    data.append(result)
            elif action == 'add_base':
                f = Producto_baseForm(request.POST)
                data = self.save_data(f)
            elif action == 'get':
                data = []
                pk = request.POST['id']
                query = Producto_base.objects.get(id=pk)
                item = query.toJSON()
                # item['presentacion'] = query.toJSON()
                data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            var = f.save()
            data['producto_base'] = var.toJSON()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'form' not in data:
            data['form'] = self.form_class(self.request.GET)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Producto'
        data['titulo'] = 'Nuevo Registro de un Producto'
        data['nuevo'] = '/producto/nuevo'
        data['action'] = 'add'
        data['crud'] = crud
        data['form_cat'] = CategoriaForm
        data['form_prod'] = Producto_baseForm
        data['form_talla'] = TallaForm
        data['form_color'] = ColorForm
        data['empresa'] = empresa
        return data


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = 'producto:lista'
    template_name = 'front-end/producto/producto_form.html'
    permission_required = 'producto.change_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            pk = self.kwargs.get('pk', 0)
            producto = self.model.objects.get(id=pk)
            f = self.form_class(request.POST or None, request.FILES or None, instance=producto)
            if f.is_valid():
                if Producto.objects.filter(producto_base_id=f.data['producto_base'], color_id=f.data['color'],
                                           talla_id=f.data['talla']).exclude(id=pk):
                    f.add_error("producto_base", "Prenda de vestir repetida")
                    data['error'] = f.errors
                else:
                    var = f.save()
                    data['producto_base'] = var.toJSON()
                    data['resp'] = True
            else:
                data['error'] = f.errors
                data['form'] = f
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        producto = self.model.objects.get(id=pk)
        if 'form' not in data:
            data['form'] = self.form_class(instance=producto)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Producto'
        data['action'] = 'edit'
        data['crud'] = '/producto/editar/' + str(self.kwargs['pk'])
        data['empresa'] = empresa
        data['form_cat'] = CategoriaForm
        data['form_prod'] = Producto_baseForm
        data['form_talla'] = TallaForm
        data['form_color'] = ColorForm
        return data


@csrf_exempt
def index(request):
    data = {}
    try:
        data = []
        for p in Producto.objects.filter(stock__range=[1, 10]):
            data.append(p.toJSON())
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_prod(request):
    data = {}
    try:
        data = []
        id = request.POST['id']
        producto = Producto.objects.filter(pk=id)
        empresa = Empresa.objects.first()
        for i in producto:
            item = i.toJSON()
            item['cantidad'] = 1
            item['subtotal'] = 0.00
            item['iva_emp'] = empresa.iva
            data.append(item)
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)
