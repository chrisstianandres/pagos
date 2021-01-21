import json

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa

from apps.mixins import ValidatePermissionRequiredMixin
from apps.talla.forms import TallaForm
from apps.talla.models import Talla

opc_icono = 'fas fa-boxes'
opc_entidad = 'Talla'
crud = '/talla/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Talla
    template_name = 'front-end/talla/talla_list.html'
    permission_required = 'talla.view_talla'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Talla.objects.all():
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
        data['boton'] = 'Nueva Talla'
        data['titulo'] = 'Listado de Tallas'
        data['nuevo'] = '/talla/nuevo'
        data['empresa'] = empresa
        data['form'] = TallaForm()
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = TallaForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                f = TallaForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                cat = Talla.objects.get(pk=int(pk))
                f = TallaForm(request.POST, instance=cat)
                data = self.edit_data(f, pk)
            elif action == 'delete':
                cat = Talla.objects.get(pk=pk)
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
            if Talla.objects.filter(talla=f.data['talla']):
                f.add_error("talla", "Ya existe una talla similar")
                data['error'] = f.errors
            elif Talla.objects.filter(eqv_letra=f.data['eqv_letra']):
                f.add_error("eqv_letra", "Ya existe una talla con letras iguales similar")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['talla'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def edit_data(self, f, pk):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if Talla.objects.filter(talla=f.data['talla']).exclude(pk=pk):
                f.add_error("talla", "Ya existe un tipo de material con este nombre")
                data['error'] = f.errors
            elif Talla.objects.filter(eqv_letra=f.data['eqv_letra']).exclude(pk=pk):
                f.add_error("eqv_letra", "Ya existe una talla con letras iguales similar")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['talla'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data
