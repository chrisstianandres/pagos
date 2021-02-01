import json

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.color.forms import ColorForm
from apps.color.models import Color
from apps.mixins import ValidatePermissionRequiredMixin

opc_icono = 'fas fa-palette'
opc_entidad = 'Color'
crud = '/color/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Color
    template_name = 'front-end/color/color_list.html'
    permission_required = 'color.view_color'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Color.objects.all():
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
        data['boton'] = 'NuevO Color'
        data['titulo'] = 'Listado de Colores'
        data['nuevo'] = '/color/nuevo'
        data['empresa'] = empresa
        data['form'] = ColorForm
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = ColorForm
    template_name = 'front-end/color/color_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']

        try:
            if action == 'add':
                f = ColorForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                pk = request.POST['id']
                cat = Color.objects.get(pk=int(pk))
                f = ColorForm(request.POST, instance=cat)
                data = self.edit_data(f, pk)
            elif action == 'delete':
                pk = request.POST['id']
                cat = Color.objects.get(pk=pk)
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
            var = f.save()
            data['resp'] = True
            data['color'] = var.toJSON()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def edit_data(self, f, pk):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if Categoria.objects.filter(nombre__icontains=f.data['nombre']).exclude(pk=pk):
                f.add_error("nombre", "Ya existe una categoria este nombre")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['categoria'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data
