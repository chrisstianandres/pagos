import json

from django.db.models import Q, Sum, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.asignar_recursos.models import Detalle_asig_recurso
from apps.backEnd import nombre_empresa
from apps.categoria.forms import CategoriaForm
from apps.inventario_material.models import Inventario_material
from apps.material.forms import MaterialForm, Producto_baseForm
from apps.material.models import Material
from apps.mixins import ValidatePermissionRequiredMixin
from apps.presentacion.forms import PresentacionForm
from apps.producto_base.models import Producto_base

opc_icono = 'fas fa-hat-cowboy-side'
opc_entidad = 'Material'
crud = '/material/nuevo'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Material
    template_name = 'front-end/material/material_list.html'
    permission_required = 'material.view_material'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Material.objects.all():
                    data.append(c.toJSON())
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Material.objects.filter(Q(producto_base__nombre__icontains=term))[0:10]
                for a in query:
                    result = {'id': int(a.id), 'text': str(a.producto_base.nombre)}
                    data.append(result)
            elif action == 'search_perd':
                data = []
                term = request.POST['term']
                asig = request.POST['asig[id]']

                query = Detalle_asig_recurso.\
                            objects.filter(inventario_material__material__producto_base__nombre__icontains=term, asig_recurso_id=int(asig)).\
                            values('inventario_material__material__producto_base_id',
                                   'asig_recurso_id',
                                   'inventario_material__material_id'
                                   ).annotate(total=Count('id')).\
                            order_by('-total')[0:10]
                for i in query:
                    px = Producto_base.objects.get(id=int(i['inventario_material__material__producto_base_id']))
                    result = {'id': int(i['asig_recurso_id']), 'text': str(px.nombre)}
                    data.append(result)
            elif action == 'get':
                id = request.POST['id']
                asig = request.POST['asig[id]']
                material = Detalle_asig_recurso.objects.filter(asig_recurso_id=int(asig)).values('inventario_material__material__producto_base')
                print(material)
                data = []
                # for i in material:
                #     item = i.toJSON()
                #     item['cantidad'] = 1
                #     item['subtotal'] = 0.00
                #     item['iva_emp'] = 12
                #     cal = format(float((i.p_compra*100)/112), '.2f')
                #     item['p_compra'] = cal
                #     data.append(item)
            elif action == 'search_asig':
                data = []
                term = request.POST['term']
                query = Material.objects.filter(Q(producto_base__nombre__icontains=term, producto_base__stock__gte=1))[0:10]
                for a in query:
                    result = {'id': int(a.id), 'text': str(a.producto_base.nombre)}
                    data.append(result)
            elif action == 'get_asig':
                id = request.POST['id']
                material = Material.objects.filter(pk=id)
                data = []
                for i in material:
                    item = i.toJSON()
                    item['cantidad'] = 1
                    data.append(item)
            elif action == 'get_perd':
                id = request.POST['id']
                material = Detalle_asig_recurso.objects.filter(asig_recurso_id=id).\
                    values('inventario_material__material__producto_base_id').annotate(total=Count('id')).\
                            order_by('-total')
                producto = Detalle_asig_recurso.objects.filter(asig_recurso_id=id). \
                    values('inventario_material__material_id').annotate(total=Count('id')). \
                    order_by('-total')
                py = ''
                for x in producto:
                    py = int(x['inventario_material__material_id'])
                data = []
                for i in material:
                    px = Producto_base.objects.get(id=int(i['inventario_material__material__producto_base_id']))
                    item = px.toJSON()
                    item['id'] = py
                    item['cantidad'] = 1
                    item['max'] = int(i['total'])
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Material'
        data['titulo'] = 'Listado de Materiales'
        data['nuevo'] = '/material/nuevo'
        data['empresa'] = empresa
        return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Material
    template_name = 'front-end/material/material_report.html'
    permission_required = 'material.view_material'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                data = []
                for c in Material.objects.all():
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
        data['titulo'] = 'Reporte de Materiales'
        data['empresa'] = empresa
        return data


class Createview(ValidatePermissionRequiredMixin, CreateView):
    model = Producto_base
    second_model = Material
    form_class = Producto_baseForm
    second_form_class = MaterialForm
    success_url = 'material:lista'
    template_name = 'front-end/material/material_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                self.object = self.get_object
                f = self.form_class(request.POST)
                f2 = self.second_form_class(request.POST)
                data = self.save_data(f, f2)
                return HttpResponseRedirect(reverse_lazy('material:lista'))
            elif action == 'delete':
                pk = request.POST['id']
                f = Material.objects.get(pk=pk)
                f2 = Producto_base.objects.get(id=f.producto_base_id)
                f.delete()
                f2.delete()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f, f2):
        data = {}
        if f.is_valid() and f2.is_valid():
            base = f2.save(commit=False)
            base.producto_base = f.save()
            base.save()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'form' not in data:
            data['form'] = self.form_class(self.request.GET)
        if 'form2' not in data:
            data['form2'] = self.second_form_class(self.request.GET)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Material'
        data['titulo'] = 'Nuevo Registro de un Material'
        data['nuevo'] = '/material/nuevo'
        data['action'] = 'add'
        data['crud'] = crud
        data['form_cat'] = CategoriaForm
        data['form_pres'] = PresentacionForm
        data['empresa'] = empresa
        return data


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    second_model = Producto_base
    second_form_class = Producto_baseForm
    success_url = reverse_lazy('material:lista')
    template_name = 'front-end/material/material_form.html'
    permission_required = 'material.change_material'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            material = self.model.objects.get(id=pk)
            producto_base = self.second_model.objects.get(id=material.producto_base_id)
            if action == 'edit':
                f = self.second_form_class(request.POST, instance=producto_base)
                f2 = self.form_class(request.POST, instance=material)
                data = self.save_data(f, f2)
                return HttpResponseRedirect(reverse_lazy('material:lista'))
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f, f2):
        data = {}
        if f.is_valid() and f2.is_valid():
            f.save()
            f2.save()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super(Updateview, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        material = self.model.objects.get(id=pk)
        producto_base = self.second_model.objects.get(id=material.producto_base_id)
        data['form'] = self.second_form_class(instance=producto_base)
        data['form2'] = self.form_class(instance=material)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Material'
        data['action'] = 'edit'
        data['crud'] = '/material/editar/' + str(self.kwargs['pk'])
        data['form_cat'] = CategoriaForm
        data['form_pres'] = PresentacionForm
        data['empresa'] = empresa
        return data

# class lista(ListView):
#     model = Producto
#     template_name = 'front-end/material/material_list.html'
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['icono'] = opc_icono
#         data['entidad'] = opc_entidad
#         data['boton'] = 'Nuevo Material'
#         data['titulo'] = 'Listado de Materiales'
#         data['nuevo'] = '/material/nuevo'
#         data['empresa'] = empresa
#         return data
#
#
# def nuevo(request):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
#         'boton': 'Guardar Producto', 'action': 'add', 'titulo': 'Nuevo Registro de un Producto',
#     }
#     if request.method == 'GET':
#         data['form'] = ProductoForm()
#     return render(request, 'front-end/producto/producto_form.html', data)
#
#
# def crear(request):
#     f = ProductoForm(request.POST)
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
#         'boton': 'Guardar Producto', 'action': 'add', 'titulo': 'Nuevo Registro de un Producto'
#     }
#     action = request.POST['action']
#     data['action'] = action
#     if request.method == 'POST':
#         f = ProductoForm(request.POST)
#         if f.is_valid():
#             f.save()
#         else:
#             data['form'] = f
#             return render(request, 'front-end/producto/producto_form.html', data)
#         return HttpResponseRedirect('/producto/lista')
#
#
# def editar(request, id):
#     producto = Producto.objects.get(id=id)
#     crud = '/producto/editar/' + str(id)
#     data = {
#         'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa': empresa,
#         'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Producto',
#     }
#     if request.method == 'GET':
#         form = ProductoForm(instance=producto)
#         data['form'] = form
#     else:
#         form = ProductoForm(request.POST, instance=producto)
#         if form.is_valid():
#             form.save()
#         else:
#             data['form'] = form
#         return redirect('/producto/lista')
#     return render(request, 'front-end/producto/producto_form.html', data)
#
#
# @csrf_exempt
# def eliminar(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             ps = Producto.objects.get(pk=id)
#             ps.delete()
#             data['resp'] = True
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = "!No se puede eliminar este producto porque esta referenciado en otros procesos!!"
#         data['content'] = "Intenta con otro producto"
#     return JsonResponse(data)

#
# @csrf_exempt
# def index(request):
#     data = {}
#     try:
#         data = []
#         for p in Producto.objects.filter(stock__lt=10):
#             data.append(p.toJSON())
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)
