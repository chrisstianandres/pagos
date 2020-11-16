from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.gasto.forms import GastoForm
from apps.gasto.models import Gasto

opc_icono = 'fas fa-file-invoice-dollar'
opc_entidad = 'Gasto'
crud = '/gasto/crear'
empresa = nombre_empresa()


class lista(ListView):
    model = Gasto
    template_name = 'front-end/gasto/gasto_list.html'

    def get_context_data(self, **kwargs):
        print()
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Gasto'
        data['titulo'] = 'Listado de Gastos'
        data['nuevo'] = '/gasto/nuevo'
        data['empresa'] = empresa
        return data


@csrf_exempt
def data(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            gasto = Gasto.objects.all()
            for c in gasto:
                data.append([
                    c.id,
                    c.fecha.strftime('%d-%m-%Y'),
                    c.tipo_gasto.nombre,
                    format(c.valor, '.2f'),
                    c.detalle,
                    c.id
                ])
        else:
            gasto = Gasto.objects.filter(fecha__range=[start_date, end_date])
            for c in gasto:
                data.append([
                    c.id,
                    c.fecha.strftime('%d-%m-%Y'),
                    c.tipo_gasto.nombre,
                    format(c.valor, '.2f'),
                    c.detalle,
                    c.id
                ])
    except:
        pass
    return JsonResponse(data, safe=False)


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Gasto', 'action': 'add', 'titulo': 'Nuevo Registro de un Gasto',
    }
    if request.method == 'GET':
        data['form'] = GastoForm()
    return render(request, 'front-end/gasto/gasto_form.html', data)


def crear(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Gasto', 'action': 'add', 'titulo': 'Nuevo Registro de un Gasto'
    }
    if request.method == 'POST':
        f = GastoForm(request.POST)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect('/gasto/lista')
        else:
            data['form'] = f
    return render(request, 'front-end/gasto/gasto_form.html', data)


def editar(request, id):
    gasto = Gasto.objects.get(id=id)
    crud = '/gasto/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa': empresa,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Gasto',
    }
    if request.method == 'GET':
        form = GastoForm(instance=gasto)
        data['form'] = form
    else:
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/gasto/lista')
    return render(request, 'front-end/gasto/gasto_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Gasto.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = "!No se puede eliminar este gasto porque esta referenciado en otros procesos!!"
        data['content'] = "Intenta con otro Gasto"
    return JsonResponse(data)


@csrf_exempt
def data_report_total(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            query = Gasto.objects.values('id', 'fecha', 'tipo_gasto__nombre', 'detalle').annotate(Sum('valor'))
            for p in query:
                data.append([
                    p['id'],
                    p['fecha'].strftime("%d/%m/%Y"),
                    p['tipo_gasto__nombre'],
                    p['detalle'],
                    format(p['valor__sum'], '.2f')
                ])
        else:
            query = Gasto.objects.values('id', 'fecha', 'tipo_gasto__nombre', 'detalle').annotate(Sum('valor')).filter(
                fecha_venta__range=[start_date, end_date])
            for p in query:
                data.append([
                    p['id'],
                    p['fecha'].strftime("%d/%m/%Y"),
                    p['tipo_gasto__nombre'],
                    p['detalle'],
                    format(p['valor__sum'], '.2f')
                ])
    except:
        pass
    return JsonResponse(data, safe=False)


class report_total(ListView):
    model = Gasto
    template_name = 'front-end/gasto/gasto_report_total.html'

    def get_queryset(self):
        return Gasto.objects.none()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Gasto'
        data['titulo'] = 'Reporte de Gastos'
        data['nuevo'] = '/gasto/nuevo'
        data['empresa'] = empresa
        return data
