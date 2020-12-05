import json

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.maquina.forms import MaquinaForm, TipomaquinaForm
from apps.maquina.models import Maquina, Tipo_maquina

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
            elif action == 'search_asig':
                data = []
                term = request.POST['term']
                query = Maquina.objects.filter(Q(tipo__nombre__icontains=term) | Q(serie__icontains=term), estado=0)[0:10]
                for a in query:
                    result = {'id': int(a.id), 'text': str(a.tipo.nombre)}
                    data.append(result)
            elif action == 'get_asig':
                id = request.POST['id']
                material = Maquina.objects.filter(pk=id)
                data = []
                for i in material:
                    item = i.toJSON()
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
        data['boton'] = 'Nueva maquina'
        data['titulo'] = 'Listado de Maquina'
        data['nuevo'] = '/maquina/nuevo'
        data['empresa'] = empresa
        data['action'] = 'add'
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = MaquinaForm
    template_name = 'front-end/maquina/maquna_form.html'
    permission_required = 'maquina.add_maquina'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = MaquinaForm(request.POST)
                data = self.save_data(f)
                return HttpResponseRedirect('/maquina/lista')
            if action == 'add_tipo':
                f = TipomaquinaForm(request.POST)
                data = self.save_data(f)
            elif action == 'delete':
                pk = request.POST['id']
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
            var = f.save()
            data['tipo'] = var.toJSON()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar maquina'
        data['titulo'] = 'Nueva maquina'
        data['empresa'] = empresa
        data['action'] = 'add'
        data['form'] = MaquinaForm
        data['form_tipo'] = TipomaquinaForm
        return data


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    form_class = MaquinaForm
    model = Maquina
    template_name = 'front-end/maquina/maquna_form.html'
    permission_required = 'maquina.change_maquina'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                pk = self.kwargs['pk']
                tpg = Maquina.objects.get(pk=int(pk))
                f = MaquinaForm(request.POST, instance=tpg)
                data = self.save_data(f)
                return HttpResponseRedirect('/maquina/lista')
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            var = f.save()
            data['tipo'] = var.toJSON()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar maquina'
        data['titulo'] = 'Editar maquina'
        data['empresa'] = empresa
        data['action'] = 'edit'
        maquina = Maquina.objects.get(id=self.kwargs['pk'])
        print(maquina.serie)
        data['crud'] = '/maquina/editar/' + str(self.kwargs['pk'])
        data['form'] = MaquinaForm(instance=maquina)
        data['form_tipo'] = TipomaquinaForm()
        return data
