import json

from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.tipogasto.forms import TipogastoForm
from apps.tipogasto.models import Tipo_gasto

opc_icono = 'far fa-keyboard'
opc_entidad = 'Tipo de Gasto'
crud = '/tipo_gasto/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Tipo_gasto
    template_name = 'front-end/tipo_gasto/tipo_gasto_list.html'
    permission_required = 'tipo_gasto.view_tipo_gasto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Tipo_gasto.objects.all():
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
        data['boton'] = 'Nuevo Tipo de gasto'
        data['titulo'] = 'Listado de Tipos de Gastos'
        data['nuevo'] = '/tipo_gasto/nuevo'
        data['empresa'] = empresa
        data['form'] = TipogastoForm
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = TipogastoForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                f = TipogastoForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                tpg = Tipo_gasto.objects.get(pk=int(pk))
                f = TipogastoForm(request.POST, instance=tpg)
                data = self.save_data(f)
            elif action == 'delete':
                cat = Tipo_gasto.objects.get(pk=pk)
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
            f.save()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data
