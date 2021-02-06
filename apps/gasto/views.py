import json

from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.gasto.forms import GastoForm
from apps.gasto.models import Gasto
from apps.mixins import ValidatePermissionRequiredMixin

opc_icono = 'fas fa-file-invoice-dollar'
opc_entidad = 'Gasto'
crud = '/gasto/crear'
empresa = nombre_empresa()

class lista(ValidatePermissionRequiredMixin, ListView):
    model = Gasto
    template_name = 'front-end/gasto/gasto_list.html'
    permission_required = 'gasto.view_gasto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        try:
            data = []
            if start_date == '' and end_date == '':
                gasto = Gasto.objects.all()
            else:
                gasto = Gasto.objects.filter(fecha_pago__range=[start_date, end_date])
            for c in gasto:
                data.append(c.toJSON())
            print(data)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo gasto'
        data['titulo'] = 'Listado de Gastos'
        data['nuevo'] = '/gasto/nuevo'
        data['empresa'] = empresa
        data['form'] = GastoForm
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = GastoForm
    permission_required = 'gasto.view_gasto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                f = GastoForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                tpg = Gasto.objects.get(pk=int(pk))
                f = GastoForm(request.POST, instance=tpg)
                data = self.save_data(f)
            elif action == 'delete':
                cat = Gasto.objects.get(pk=pk)
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


class report_total(ListView):
    model = Gasto
    template_name = 'front-end/gasto/gasto_report_total.html'
    permission_required = 'gasto.view_gasto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Gasto.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                if start_date == '' and end_date == '':
                    query = Gasto.objects.values('id', 'fecha_pago', 'tipo_gasto__nombre', 'detalle').annotate(Sum('valor'))
                else:
                    query = Gasto.objects.filter(fecha_pago__range=[start_date, end_date])\
                        .values('id', 'fecha_pago', 'tipo_gasto__nombre', 'detalle').annotate(Sum('valor'))
                for p in query:
                    data.append([
                        p['id'],
                        p['fecha_pago'].strftime("%d/%m/%Y"),
                        p['tipo_gasto__nombre'],
                        p['detalle'],
                        format(p['valor__sum'], '.2f')
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Gasto'
        data['titulo'] = 'Reporte de Gastos'
        data['nuevo'] = '/gasto/nuevo'
        data['empresa'] = empresa
        return data
