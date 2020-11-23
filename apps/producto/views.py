import json

from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

# from apps.Mixins import SuperUserRequiredMixin
from apps.backEnd import nombre_empresa
from apps.categoria.forms import CategoriaForm
from apps.mixins import ValidatePermissionRequiredMixin
from apps.presentacion.forms import PresentacionForm
from apps.producto.forms import ProductoForm
from apps.producto.models import Producto

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
    model = Producto
    form_class = ProductoForm
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
                f = ProductoForm(request.POST)
                data = self.save_data(f)
                return HttpResponseRedirect('/producto/lista')
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            f.save()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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
    model = Producto
    form_class = ProductoForm
    success_url = 'producto:lista'
    template_name = 'front-end/producto/producto_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            producto = Producto.objects.get(pk = self.kwargs['pk'])
            if action == 'edit':
                f = ProductoForm(request.POST, instance= producto)
                data = self.save_data(f)
                return HttpResponseRedirect('/producto/lista')
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            f.save()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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
