import json

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.categoria.forms import CategoriaForm
from apps.empresa.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.presentacion.forms import PresentacionForm
from apps.producto.forms import ProductoForm, Producto_baseForm
from apps.producto.models import Producto
from apps.producto_base.models import Producto_base

opc_icono = 'fab fa-amazon'
opc_entidad = 'Productos'
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
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Producto.objects.filter(producto_base__nombre__icontains=term, producto_base__stock__gte=1)[0:10]
                for a in query:
                    result = {'id': int(a.id), 'text': str(a.producto_base.nombre)}
                    data.append(result)
            elif action == 'search_rep':
                data = []
                term = request.POST['term']
                query = Producto.objects.filter(producto_base__nombre__icontains=term)[0:10]
                for a in query:
                    result = {'id': int(a.id), 'text': str(a.producto_base.nombre)}
                    data.append(result)
            elif action == 'get':
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


class Createview(ValidatePermissionRequiredMixin, CreateView):
    model = Producto_base
    second_model = Producto
    form_class = Producto_baseForm
    second_form_class = ProductoForm
    success_url = 'producto:lista'
    template_name = 'front-end/producto/producto_form.html'

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
                return HttpResponseRedirect('/producto/lista')
            elif action == 'delete':
                pk = request.POST['id']
                f = Producto.objects.get(pk=pk)
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
        data['boton'] = 'Guardar Producto'
        data['titulo'] = 'Nuevo Registro de un Producto'
        data['nuevo'] = '/producto/nuevo'
        data['action'] = 'add'
        data['crud'] = crud
        data['form_cat'] = CategoriaForm
        data['form_pres'] = PresentacionForm
        data['empresa'] = empresa
        return data


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    model = Producto_base
    form_class = Producto_baseForm
    second_model = Producto
    second_form_class = ProductoForm
    success_url = 'producto:lista'
    template_name = 'front-end/producto/producto_form.html'
    permission_required = 'producto.change_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            producto = self.second_model.objects.get(id=pk)
            producto_base = self.model.objects.get(id=producto.producto_base_id)
            if action == 'edit':
                f = self.form_class(request.POST, instance=producto_base)
                f2 = self.second_form_class(request.POST, instance=producto)
                data = self.save_data(f, f2)
                return HttpResponseRedirect('/producto/lista')
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
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        producto = self.second_model.objects.get(id=pk)
        producto_base = self.model.objects.get(id=producto.producto_base_id)
        if 'form' not in data:
            data['form'] = self.form_class(instance=producto_base)
        if 'form2' not in data:
            data['form2'] = self.second_form_class(instance=producto)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Producto'
        data['action'] = 'edit'
        data['crud'] = '/producto/editar/' + str(self.kwargs['pk'])
        data['form_cat'] = CategoriaForm
        data['form_pres'] = PresentacionForm
        data['empresa'] = empresa
        return data
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

@csrf_exempt
def index(request):
    data = {}
    try:
        data = []
        for p in Producto.objects.filter(stock__lt=10):
            data.append(p.toJSON())
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)
