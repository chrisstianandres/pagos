import json

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, request
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView

from apps.backEnd import nombre_empresa
from apps.cliente.models import Cliente
from apps.mixins import ValidatePermissionRequiredMixin
from apps.user.forms import UserForm
from apps.user.models import User
from apps.proveedor.models import Proveedor

opc_icono = 'fas fa-user-shield'
opc_entidad = 'Usuarios'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'front-end/empleado/empleado_list.html'
    permission_required = 'user.view_user'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                user = User.objects.all()
                for c in user:
                    data.append(c.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Usuario'
        data['titulo'] = 'Listado de Usuarios'
        data['nuevo'] = '/usuario/nuevo'
        data['form'] = UserForm
        data['empresa'] = empresa
        return data
@csrf_exempt
def data(request):
    data = []
    try:
        empleado = User.objects.all()
        for c in empleado:
            data.append([
                c.id,
                c.username,
                c.get_full_name(),
                c.cedula,
                c.cargo.nombre,
                c.direccion,
                c.telefono,
                c.get_sexo_display(),
                c.get_estado_display(),
                c.id,
            ])

    except:
        pass
    return JsonResponse(data, safe=False)


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Empleado', 'action': 'add', 'titulo': 'Nuevo Registro de un Empleado',
        'option': 'add'
    }
    if request.method == 'GET':
        data['form'] = UserForm()
    return render(request, 'front-end/empleado/empleado_form.html', data)


def crear(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa' : empresa,
        'boton': 'Guardar Empleado', 'action': 'add', 'titulo': 'Nuevo Registro de un Empleado', 'option': 'add'
    }
    action = request.POST['action']
    data['action'] = action
    if request.method == 'POST' and 'action' in request.POST:
        if action == 'add':
            f = UserForm(request.POST, request.FILES)

            if f.is_valid():
                f.save(commit=False)
                if Proveedor.objects.filter(tipo=0, num_doc=f.data['cedula']):
                    data['error'] = 'Numero de Cedula ya exitente en los Proveedores'
                    data['form'] = f
                elif Cliente.objects.filter(cedula=f.data['cedula']):
                    data['error'] = 'Numero de Cedula ya exitente en los Clientes'
                    data['form'] = f
                elif verificar(f.data['cedula']):
                    if int(f.data['cargo']) == 1:
                        f.save()
                        nw = f.save()
                        ch = User.objects.get(pk=nw.pk)
                        ch.is_superuser = 1
                        ch.save()
                    else:
                        f.save()
                        nw = f.save()
                        ch = User.objects.get(pk=nw.pk)
                        ch.is_superuser = 0
                        ch.save()
                    return HttpResponseRedirect('/empleado/lista')
                else:
                    data['error'] = 'Numero de Cedula no valido para Ecuador'
                    data['form'] = f
            else:
                data['form'] = f
            return render(request, 'front-end/empleado/empleado_form.html', data)


def editar(request, id):
    empleado = User.objects.get(id=id)
    crud = '/user/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa' : empresa,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Empleado',
        'option': 'editar'
    }
    if request.method == 'GET':
        form = UserForm(instance=empleado)
        data['form'] = form
    else:
        form = UserForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save(commit=False)
            form.save()
        else:
            data['form'] = form

        return HttpResponseRedirect('/empleado/lista')
    return render(request, 'front-end/empleado/empleado_form.html', data)


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = 'user:lista'
    template_name = 'front-end/empleado/empleado_form.html'
    permission_required = 'user.change_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            user = self.model.objects.get(id=pk)
            data = {
                'icono': opc_icono, 'crud': '/user/editar/' + str(self.kwargs['pk']), 'entidad': opc_entidad, 'empresa': empresa,
                'boton': 'Guardar Edicion', 'titulo': 'Edicion del Registro de un Usuario',
                'action': 'edit'
            }
            if action == 'edit':
                f = self.form_class(request.POST, request.FILES, instance=user)
                if f.is_valid():
                    f.save(commit=False)
                    if Proveedor.objects.filter(tipo=0, num_doc=f.data['cedula']):
                        f.add_error("cedula", "Numero de Cedula ya exitente en los Proveedores")
                        data['form'] = f
                        return render(request, 'front-end/empleado/empleado_form.html', data)
                    elif Cliente.objects.filter(cedula=f.data['cedula']):
                        f.add_error("cedula", "Numero de Cedula ya exitente en los Clientes")
                        data['form'] = f
                        return render(request, 'front-end/empleado/empleado_form.html', data)
                    elif verificar(f.data['cedula']):
                        f.save()
                        data['resp'] = True
                    else:
                        f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                        data['error'] = f.errors
                        data['form'] = f
                        return render(request, 'front-end/empleado/empleado_form.html', data)
                else:
                    data['form'] = f
                    data['error'] = f.errors
                    return render(request, 'front-end/empleado/empleado_form.html', data)
                return HttpResponseRedirect('/user/lista')
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        user = self.model.objects.get(id=pk)
        data['form'] = self.form_class(instance=user)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Usuario'
        data['action'] = 'edit'
        data['crud'] = '/user/editar/' + str(self.kwargs['pk'])
        data['empresa'] = empresa
        return data

@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = User.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = 'No se puede eliminar este cliente porque esta referenciado en otros procesos'
        data['content'] = 'Intenta con otro cliente'
    return JsonResponse(data)


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


@csrf_exempt
def estado(request):
    data = {}
    try:
        id = int(request.POST['id'])
        ps = User.objects.get(pk=id)
        if ps.estado == 1:
            ps.estado = 0
            ps.save()
            data['resp'] = True
        elif ps.estado == 0:
            ps.estado = 1
            ps.save()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


def profile(request):
    empleado = User.objects.get(id=request.user.id)
    crud = '/user/profile'
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Uusuario', 'action': 'add', 'titulo': 'Perfil de Usuario', 'empresa': nombre_empresa()
    }
    if request.method == 'GET':
        form = UserForm(instance=empleado)
        data['form'] = form
    else:
        form = UserForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/profile')
        else:
            data['form'] = form
    return render(request, 'front-end/profile.html', data)
        # return render(request, 'front-end/profile.html', data)
