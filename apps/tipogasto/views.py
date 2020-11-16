from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.tipogasto.forms import TipogastoForm
from apps.tipogasto.models import Tipo_gasto

opc_icono = 'far fa-keyboard'
opc_entidad = 'Tipo de Gasto'
crud = '/tipo_gasto/crear'
empresa = nombre_empresa()


class lista(ListView):
    model = Tipo_gasto
    template_name = 'front-end/tipo_gasto/tipo_gasto_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Tipo de gasto'
        data['titulo'] = 'Listado de Tipos de Gastos'
        data['nuevo'] = '/tipo_gasto/nuevo'
        data['empresa'] = empresa
        return data


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Tipo de gasto', 'action': 'add', 'titulo': 'Nuevo Registro de un Tipo de gasto',
    }
    if request.method == 'GET':
        data['form'] = TipogastoForm()
    return render(request, 'front-end/tipo_gasto/tipo_gasto_form.html', data)


def crear(request):
    f = TipogastoForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Tipo de gasto', 'action': 'add', 'titulo': 'Nuevo Registro de un Tipo de gasto',
    }
    if request.method == 'POST':
        f = TipogastoForm(request.POST)
        if f.is_valid():
            f.save()
        else:
            data['form'] = f
            return render(request, 'front-end/tipo_gasto/tipo_gasto_form.html', data)
        return HttpResponseRedirect('/tipo_gasto/lista')


def editar(request, id):
    tipo = Tipo_gasto.objects.get(id=id)
    crud = '/tipo_gasto/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa': empresa,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Tipo de Gasto',
    }
    if request.method == 'GET':
        form = TipogastoForm(instance=tipo)
        data['form'] = form
    else:
        form = TipogastoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/tipo_gasto/lista')
    return render(request, 'front-end/tipo_gasto/tipo_gasto_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Tipo_gasto.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = "!No se puede eliminar este Tipo de Gasto porque esta referenciado en otros procesos!!"
        data['content'] = "Intenta con otro Tipo de Gasto"
    return JsonResponse(data)