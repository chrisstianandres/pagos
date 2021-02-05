import json

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.tipo_material.forms import Tipo_materialForm
from apps.tipo_material.models import Tipo_material

opc_icono = 'fas fa-boxes'
opc_entidad = 'Tipo de Material'
crud = '/tipo_mat/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Tipo_material
    template_name = 'front-end/tipo_material/tipo_material_list.html'
    permission_required = 'tipo_material.view_tipo_material'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Tipo_material.objects.all():
                    data.append(c.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Tipo de Material'
        data['titulo'] = 'Listado de Tipos de Materiales'
        data['nuevo'] = '/tipo_mat/nuevo'
        data['empresa'] = empresa
        data['form'] = Tipo_materialForm()
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Tipo_materialForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = Tipo_materialForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                pk = request.POST['id']
                cat = Tipo_material.objects.get(pk=int(pk))
                f = Tipo_materialForm(request.POST, instance=cat)
                data = self.edit_data(f, pk)
            elif action == 'delete':
                pk = request.POST['id']
                cat = Tipo_material.objects.get(pk=pk)
                cat.delete()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if Tipo_material.objects.filter(nombre__icontains=f.data['nombre']):
                f.add_error("nombre", "Ya existe un tipo de material con este nombre")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['tipo_material'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def edit_data(self, f, pk):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if Tipo_material.objects.filter(nombre__icontains=f.data['nombre']).exclude(pk=pk):
                f.add_error("nombre", "Ya existe un tipo de material con este nombre")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['tipo_material'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data
