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

from apps.user.models import User
from apps.proveedor.models import Proveedor


opc_icono = 'fa fa-user'
opc_entidad = 'Clientes'
crud = '/cliente/nuevo'
empresa = nombre_empresa()


class lista(ListView):
    model = Cliente
    template_name = "front-end/cliente/cliente_list.html"

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
            elif action == data:
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
        data['titulo_new'] = 'Nuevo registro de un Cliente'
        data['form'] = ClienteForm
        data['nuevo'] = '/cliente/nuevo'
        data['empresa'] = empresa
        return data


# def nuevo(request):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
#         'boton': 'Guardar Cliente', 'action': 'add', 'titulo': 'Nuevo Registro de un Cliente',
#     }
#     if request.method == 'GET':
#         data['form'] = ClienteForm()
#     return render(request, 'front-end/cliente/cliente_form.html', data)
#
#
# def crear(request):
#     f = ClienteForm(request.POST)
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
#         'boton': 'Guardar Cliente', 'action': 'add', 'titulo': 'Nuevo Registro de un Cliente'
#     }
#     action = request.POST['action']
#     data['action'] = action
#     if request.method == 'POST' and 'action' in request.POST:
#         if action == 'add':
#             f = ClienteForm(request.POST)
#             if f.is_valid():
#                 f.save(commit=False)
#                 if Proveedor.objects.filter(documento=0, numero_documento=f.data['cedula']):
#                     data['error'] = 'Numero de Cedula ya exitente en los Proveedores'
#                     data['form'] = f
#                 elif User.objects.filter(cedula=f.data['cedula']):
#                     data['error'] = 'Numero de Cedula ya exitente en los Usuarios'
#                     data['form'] = f
#                 elif verificar(f.data['cedula']):
#                     f.save()
#                     return HttpResponseRedirect('/cliente/lista')
#                 else:
#                     data['error'] = 'Numero de Cedula no valido para Ecuador'
#                     data['form'] = f
#             else:
#                 data['form'] = f
#             return render(request, 'front-end/cliente/cliente_form.html', data)


class CreateView(CreateView):
    template_name = 'front-end/cliente/cliente_form.html'
    form_class = ClienteForm
    success_url = reverse_lazy('cliente:lista')
    permission_required = 'cliente:add_cliente'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = ClienteForm(request.POST)
                if f.is_valid():
                    f.save(commit=False)
                    if Proveedor.objects.filter(documento=0, numero_documento=f.data['cedula']):
                        f.add_error("cedula", "Numero de Cedula ya exitente en los Proveedores")
                        data['error'] = f.errors
                    elif User.objects.filter(cedula=f.data['cedula']):
                        f.add_error("cedula", "Numero de Cedula ya exitente en los Clientes")
                        data['error'] = f.errors
                    elif verificar(f.data['cedula']):
                        f.save()
                        data['resp'] = True
                    else:
                        f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                        data['error'] = f.errors
                else:
                    data['error'] = f.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
            print(data)
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def crearcli(request):
    data = {}
    f = ClienteForm(request.POST)
    try:
        if request.method == 'POST':
            if Proveedor.objects.filter(documento=0, numero_documento=request.POST['cedula']):
                f.add_error("cedula", "Numero de Cedula ya exitente en los Proveedores")
                data['error'] = f.errors
            elif User.objects.filter(cedula=request.POST['cedula']):
                f.add_error("cedula", "Numero de Cedula ya exitente en los Usuarios")
                data['error'] = f.errors
            elif verificar(request.POST['cedula']):
                with transaction.atomic():
                    if f.is_valid():
                        var = f.save()
                        data['resp'] = True
                        data['cliente'] = var.toJSON()
                        return JsonResponse(data)
                    else:
                        data['error'] = f.errors
            else:
                f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                data['error'] = f.errors
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


def editar(request, id):
    cargo = Cliente.objects.get(id=id)
    crud = '/cliente/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa': empresa,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Cliente',
        'option': 'editar'
    }
    if request.method == 'GET':
        form = ClienteForm(instance=cargo)
        data['form'] = form
    else:
        form = ClienteForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return HttpResponseRedirect('/cliente/lista')
    return render(request, 'front-end/cliente/cliente_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Cliente.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = 'No se puede eliminar este cliente porque esta referenciado en otros procesos'
        data['content'] = 'Intenta con otro cliente'
    return JsonResponse(data)


@csrf_exempt
def data_report(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            query = Cliente.objects.all()
        else:
            query = Cliente.objects.filter(fecha__range=[start_date, end_date])

        for p in query:
            data.append([
                p.id,
                p.fecha.strftime("%d/%m/%Y"),
                p.nombres + " " + p.apellidos ,
                p.cedula,
                p.correo,
                p.get_sexo_display(),
                p.direccion,
                p.telefono
            ])
    except:
        pass
    return JsonResponse(data, safe=False)


class report(ListView):
    model = Cliente
    template_name = 'front-end/cliente/cliente_report.html'

    def get_queryset(self):
        return Cliente.objects.none()

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
