import json

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.maquina.forms import MaquinaForm, TipomaquinaForm
from apps.maquina.models import Maquina, Tipo_maquina, Maquina_mantenimiento

opc_icono = 'fas fa-subway'
opc_entidad = 'Maquinas'
crud = '/maquina/crear'
empresa = nombre_empresa()
year = [{'id': y, 'year': (datetime.now().year)-y}for y in range(0, 5)]


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
                ids = json.loads(request.POST['ids'])
                query = Maquina.objects.filter(Q(tipo__nombre__icontains=term) | Q(serie__icontains=term), estado=0)
                for a in query.exclude(id__in=ids)[0:10]:
                    result = {'id': int(a.id), 'text': str(a.tipo.nombre)}
                    data.append(result)
            elif action == 'search_asig_table':
                data = []
                ids = json.loads(request.POST['ids'])
                que = Maquina.objects.filter(estado=0)
                for a in que.exclude(id__in=ids):
                    data.append(a.toJSON())
            elif action == 'get_asig':
                id = request.POST['id']
                material = Maquina.objects.filter(pk=id)
                data = []
                for i in material:
                    item = i.toJSON()
                    data.append(item)
            elif action == 'add_mant':
                id = request.POST['id']
                maquina = Maquina.objects.get(pk=id)
                maquina.estado = 2
                maquina.save()
                mant = Maquina_mantenimiento()
                mant.maquina_id = maquina.id
                mant.save()
            elif action == 'close_mant':
                id = request.POST['id']
                maquina = Maquina.objects.get(pk=id)
                maquina.estado = 0
                maquina.save()
                mant = Maquina_mantenimiento.objects.get(maquina_id=id, fecha_fin=None)
                mant.fecha_fin = datetime.now()
                mant.save()
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
    seccond_model = Tipo_maquina
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
            elif action == 'add_tipo':
                f = TipomaquinaForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit_tipo':
                data = []
                pk = request.POST['id']
                tipo = self.seccond_model.objects.get(id=pk)
                data.append(tipo.toJSON())
            elif action == 'edit_tipo_save':
                data = []
                pk = request.POST['id']
                tipo = self.seccond_model.objects.get(id=pk)
                f = TipomaquinaForm(request.POST, instance=tipo)
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



class lista_mantenimiento(ValidatePermissionRequiredMixin, ListView):
    model = Maquina_mantenimiento
    template_name = 'front-end/maquina/maquina_mantenimiento_list.html'
    permission_required = 'maquina.view_maquina_mantenimiento'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                start = request.POST['start_date']
                end = request.POST['end_date']
                if start and end:
                    query = self.model.objects.filter(fecha_ingreso__range=[start, end])
                else:
                    query = self.model.objects.all()
                for c in query:
                    data.append(c.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-tools'
        data['entidad'] = 'Mantenimiento de Maquinas'
        data['titulo'] = 'Listado mantenimiento de Maquinas'
        data['nuevo'] = '/maquina/mantenimiento'
        data['empresa'] = empresa
        data['action'] = 'add'
        data['year'] = year
        return data