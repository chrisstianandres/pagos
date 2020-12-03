import json

from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.maquina.forms import MaquinaForm
from apps.maquina.models import Maquina

opc_icono = 'fas fa-subway'
opc_entidad = 'Maquinas'
crud = '/maquina/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Maquina
    template_name = 'front-end/maquina/maquina_list.html'
    permission_required = 'maquina.view_maquina'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Maquina.objects.all():
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
        data['boton'] = 'Nueva maquina'
        data['titulo'] = 'Listado de Maquina'
        data['nuevo'] = '/maquina/nuevo'
        data['empresa'] = empresa
        data['form'] = MaquinaForm
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = MaquinaForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                f = MaquinaForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                tpg = Maquina.objects.get(pk=int(pk))
                f = MaquinaForm(request.POST, instance=tpg)
                data = self.save_data(f)
            elif action == 'delete':
                cat = Maquina.objects.get(pk=pk)
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
