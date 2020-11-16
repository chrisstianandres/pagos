from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.presentacion.forms import PresentacionForm
from apps.presentacion.models import Presentacion

opc_icono = 'fas fa-box-open'
opc_entidad = 'Presentacion'
crud = '/presentacion/crear'
empresa = nombre_empresa()


class lista(ListView):
    model = Presentacion
    template_name = 'front-end/presentacion/presentacion_list.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Presentacion'
        data['titulo'] = 'Listado de Presentaciones'
        data['nuevo'] = '/presentacion/nuevo'
        data['empresa'] = empresa
        return data


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa' : empresa,
        'boton': 'Guardar Presentacion', 'action': 'add', 'titulo': 'Nuevo Registro de una Presentacion',
    }
    if request.method == 'GET':
        data['form'] = PresentacionForm()
    return render(request, 'front-end/presentacion/presentacion_form.html', data)


def crear(request):
    f = PresentacionForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Presentacion', 'action': 'add', 'titulo': 'Nuevo Registro de una Presentacion'
    }
    if request.method == 'POST':
        f = PresentacionForm(request.POST)
        if f.is_valid():
            f.save()
        else:
            data['form'] = f
            return render(request, 'front-end/presentacion/presentacion_form.html', data)
        return HttpResponseRedirect('/presentacion/lista')


def editar(request, id):
    presentacion = Presentacion.objects.get(id=id)
    crud = '/presentacion/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa' : empresa,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de una Presentacion',
    }
    if request.method == 'GET':
        form = PresentacionForm(instance=presentacion)
        data['form'] = form
    else:
        form = PresentacionForm(request.POST, instance=presentacion)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/presentacion/lista')
    return render(request, 'front-end/presentacion/presentacion_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Presentacion.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = "!No se puede eliminar esta presentacion porque esta referenciado en otros procesos!!"
        data['content'] = "Intenta con otra presentacion"
    return JsonResponse(data)

