import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView

from apps.backEnd import nombre_empresa
from apps.cliente.models import Cliente
from apps.mixins import ValidatePermissionRequiredMixin
from apps.user.models import User
from apps.proveedor.forms import ProveedorForm
from apps.proveedor.models import Proveedor

opc_icono ='fas fa-user-tag'
opc_entidad = 'Proveedor'
crud = '/proveedor/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Proveedor
    template_name = "front-end/proveedor/proveedor_list.html"
    permission_required = 'proveedor.view_proveedor'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Proveedor.objects.all():
                    data.append(c.toJSON())
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Proveedor.objects.filter(
                    Q(nombre__icontains=term) | Q(num_doc__icontains=term))[0:10]
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
        data['boton'] = 'Nuevo Porveedor'
        data['titulo'] = 'Listado de Porveedores'
        data['form'] = ProveedorForm
        data['nuevo'] = '/proveedor/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = ProveedorForm
    template_name = 'front-end/proveedor/proveedor_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                f = ProveedorForm(request.POST)
                data = self.save_data(f)
            elif action == 'edit':
                proveedor = Proveedor.objects.get(pk=int(pk))
                f = ProveedorForm(request.POST, instance=proveedor)
                data = self.save_data(f)
            elif action == 'delete':
               pro = Proveedor.objects.get(pk=pk)
               pro.delete()
               data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        print(f.data)
        if f.is_valid():
            f.save(commit=False)
            print(f.data['tipo'])
            if int(f.data['tipo']) == 0:
                if verificar(f.data['num_doc']):
                    prod = f.save()
                    data['resp'] = True
                    data['proveedor'] = prod.toJSON()
                else:
                    f.add_error("num_doc", "Numero de Cedula no valido para Ecuador")
                    data['error'] = f.errors
            else:
                if verificar(f.data['num_doc']):
                    prod = f.save()
                    data['resp'] = True
                    data['proveedor'] = prod.toJSON()
                else:
                    f.add_error("num_doc", "Numero de Cedula no valido para Ecuador")
                    data['error'] = f.errors
        else:
            data['error'] = f.errors
        return data


# def proveedor_lista(request):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad,
#         'boton': 'Nuevo Proveedor', 'titulo': 'Listado de Proveedores', 'empresa' : empresa,
#         'nuevo': '/proveedor/nuevo',
#     }
#     list = Proveedor.objects.all()
#     data['list'] = list
#     return render(request, "front-end/proveedor/proveedor_list.html", data)
#
#
# def nuevo(request):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa' : empresa,
#         'boton': 'Guardar Proveedor', 'action': 'add', 'titulo': 'Nuevo Registro de un Proveedor',
#     }
#     if request.method == 'GET':
#         data['form'] = ProveedorForm()
#     return render(request, 'front-end/proveedor/proveedor_form.html', data)
#
#
# def crear(request):
#     f = ProveedorForm(request.POST)
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa' : empresa,
#         'boton': 'Guardar Proveedor', 'action': 'add', 'titulo': 'Nuevo Registro de un Proveedor'
#     }
#     action = request.POST['action']
#     data['action'] = action
#     if request.method == 'POST' and 'action' in request.POST:
#         if action == 'add':
#             if f.is_valid():
#                 f = ProveedorForm(request.POST)
#                 f.save(commit=False)
#                 if int(f.data['documento']) == 0:
#                     if Empleado.objects.filter(cedula=f.data['numero_documento']):
#                         data['error'] = 'Numero de Documento ya exitente en los Empleados'
#                         data['form'] = f
#                     elif Cliente.objects.filter(cedula=f.data['numero_documento']):
#                         data['error'] = 'Numero de Documento ya exitente en los Clientes'
#                         data['form'] = f
#                     elif verificar(f.data['numero_documento']):
#                         f.save()
#                         return HttpResponseRedirect('/proveedor/lista')
#                     else:
#                         data['error'] = 'Numero de Cedula no valido para Ecuador'
#                         data['form'] = f
#                 else:
#                     if verificar(f.data['numero_documento']):
#                         f.save()
#                         return HttpResponseRedirect('/proveedor/lista')
#                     else:
#                         data['error'] = 'Numero de Cedula no valido para Ecuador'
#                         data['form'] = f
#             else:
#                 data['form'] = f
#             return render(request, 'front-end/proveedor/proveedor_form.html', data)


# @csrf_exempt
# def data(request):
#     data = {}
#     try:
#         data = []
#         term = request.POST['term']
#         query = Proveedor.objects.filter(Q(nombres__icontains=term) | Q(numero_documento__icontains=term))[0:10]
#         for a in query:
#             item = a.toJSON()
#             item['text'] = a.get_full_name()
#             data.append(item)
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def crearpro(request):
#     data = {}
#     try:
#         if request.method == 'POST':
#             f = ProveedorForm(request.POST)
#             if int(f.data['documento']) == 0:
#                 if Empleado.objects.filter(cedula=f.data['numero_documento']):
#                     data['error'] = 'Numero de Documento ya exitente en los Empleados'
#                 elif Cliente.objects.filter(cedula=f.data['numero_documento']):
#                     data['error'] = 'Numero de Documento ya exitente en los Clientes'
#                 elif verificar(f.data['cedula']):
#                     with transaction.atomic():
#                         f = ProveedorForm(request.POST)
#                         if f.is_valid():
#                             var = f.save()
#                             data['resp'] = True
#                             data['proveedor'] = var.toJSON()
#                             return JsonResponse(data)
#                         else:
#                             errores = []
#                             for a in f.errors:
#                                 errores.append('El campo ' + a + ' esta ya existe <br/>')
#                             data['error'] = errores
#                 else:
#                     data['error'] = 'Numero de Cedula no valido para Ecuador'
#                     data['form'] = f
#             else:
#                 if verificar(f.data['numero_documento']):
#                     with transaction.atomic():
#                         f = ProveedorForm(request.POST)
#                         if f.is_valid():
#                             var = f.save()
#                             data['resp'] = True
#                             data['proveedor'] = var.toJSON()
#                             return JsonResponse(data)
#                         else:
#                             errores = []
#                             for a in f.errors:
#                                 errores.append('El campo ' + a + ' esta ya existe <br/>')
#                             data['error'] = errores
#                 else:
#                     data['error'] = 'Numero de Ruc no valido para Ecuador'
#     except Exception as e:
#         gs = goslate.Goslate()
#         data['error'] = gs.translate(str(e), 'es')
#     return JsonResponse(data)
#
#
# def editar(request, id):
#     proveedor = Proveedor.objects.get(id=id)
#     crud = '/proveedor/editar/' + str(id)
#     data = {
#         'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa' : empresa,
#         'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Proveedor',
#         'option': 'editar'
#     }
#     if request.method == 'GET':
#         form = ProveedorForm(instance=proveedor)
#         data['form'] = form
#     else:
#         form = ProveedorForm(request.POST, instance=proveedor)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/proveedor/lista')
#         else:
#             data['form'] = form
#     return render(request, 'front-end/proveedor/proveedor_form.html', data)
#
#
# @csrf_exempt
# def eliminar(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             ps = Proveedor.objects.get(pk=id)
#             ps.delete()
#             data['resp'] = True
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = 'No se puede eliminar este cliente porque esta referenciado en otros procesos'
#         data['content'] = 'Intenta con otro cliente'
#     return JsonResponse(data)


@csrf_exempt
def data_report(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            query = Proveedor.objects.all()
        else:
            query = Proveedor.objects.filter(fecha__range=[start_date, end_date])

        for p in query:
            data.append([
                p.id,
                p.fecha.strftime("%d/%m/%Y"),
                p.nombres,
                p.get_documento_display(),
                p.numero_documento,
                p.correo,
                p.direccion,
                p.telefono
            ])
    except:
        pass
    return JsonResponse(data, safe=False)


class report(ValidatePermissionRequiredMixin, ListView):
    model = Proveedor
    template_name = 'front-end/proveedor/proveedor_report.html'
    permission_required = 'proveedor.view_proveedor'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Proveedor.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        if action == 'report':
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            try:
                if start_date == '' and end_date == '':
                    query = Proveedor.objects.all()
                else:
                    query = Proveedor.objects.filter(fecha__range=[start_date, end_date])
                for p in query:
                    data.append(p.toJSON())
                print(data)
            except:
                pass
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Proveedores'
        data['empresa'] = empresa
        return data


def verificar(nro):
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


