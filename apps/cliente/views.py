from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.http import HttpResponse, JsonResponse

from apps.backEnd import nombre_empresa
from apps.cliente.forms import ClienteForm
from apps.cliente.models import Cliente
from django.http import HttpResponseRedirect
import json
from django.db.models import Q

from apps.mixins import ValidatePermissionRequiredMixin
from apps.user.models import User
from apps.proveedor.models import Proveedor

opc_icono = 'fa fa-user'
opc_entidad = 'Clientes'
crud = '/cliente/nuevo'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Cliente
    template_name = "front-end/cliente/cliente_list.html"
    permission_required = 'cliente.view_cliente'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Cliente.objects.all():
                    data.append(c.toJSON())
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Cliente.objects.filter(
                    Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(cedula__icontains=term))[0:10]
                for a in query:
                    item = a.toJSON()
                    item['text'] = a.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Cliente'
        data['titulo'] = 'Listado de Clientes'
        data['form'] = ClienteForm
        data['nuevo'] = '/cliente/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = ClienteForm
    template_name = 'front-end/cliente/cliente_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                f = ClienteForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                cliente = Cliente.objects.get(pk=int(pk))
                f = ClienteForm(request.POST, instance=cliente)
                data = self.save_data(f)
            elif action == 'delete':
               cli = Cliente.objects.get(pk=pk)
               cli.delete()
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
            if verificar(f.data['cedula']):
                cli = f.save()
                data['resp'] = True
                data['cliente'] = cli.toJSON()
            else:
                f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                data['error'] = f.errors
        else:
            data['error'] = f.errors
        return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Cliente
    template_name = 'front-end/cliente/cliente_report.html'
    permission_required = 'cliente.view_cliente'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Cliente.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        if action == 'report':
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            try:
                if start_date == '' and end_date == '':
                    query = Cliente.objects.all()
                else:
                    query = Cliente.objects.filter(fecha__range=[start_date, end_date])

                for p in query:
                    data.append(p.toJSON())
            except:
                pass
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Clientes'
        data['empresa'] = empresa
        return data


def verificar(nro):
    error = ''
    l = len(nro)
    if l == 10 or l == 13:  # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 22:  # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(nro, 0)
                elif l == 13:
                    return __validar_ced_ruc(nro, 0) and nro[
                                                         10:13] != '000'  # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro, 1)  # sociedades publicas
            elif tercer_dig == 9:  # si es ruc
                return __validar_ced_ruc(nro, 2)  # sociedades privadas
            else:
                error = 'Tercer digito invalido'
                return False and error
        else:
            error = 'Codigo de provincia incorrecto'
            return False and error
    else:
        error = 'Longitud incorrecta del numero ingresado'
        return False and error


def __validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])  # digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0, len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver
