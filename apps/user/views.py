import json

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, request
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, TemplateView

from apps.backEnd import nombre_empresa
from apps.cliente.models import Cliente
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.forms import GroupForm
from apps.user.forms import UserForm, UserForm_online
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
            elif action == 'estado':
                id = request.POST['id']
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
            elif action == 'delete':
                try:
                    id = request.POST['id']
                    if id:
                        ps = User.objects.get(pk=id)
                        ps.delete()
                        data['resp'] = True
                    else:
                        data['error'] = 'Ha ocurrido un error'
                except Exception as e:
                    data['error'] = str(e)
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


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = UserForm
    template_name = 'front-end/empleado/empleado_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                f = UserForm(request.POST, request.FILES)
                if f.is_valid():
                    f.save(commit=False)
                    if verificar(f.data['cedula']):
                        f.save()
                        return HttpResponseRedirect('/empleado/lista')
                    else:
                        f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                        data['form'] = f
                else:
                    data['form'] = f
                return render(request, 'front-end/empleado/empleado_form.html', data)
            elif action == 'delete':
               cli = User.objects.get(pk=pk)
               cli.delete()
               data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

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
                    if verificar(f.data['cedula']):
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


class Listgroupsview(ValidatePermissionRequiredMixin, ListView):
    model = Group
    template_name = 'front-end/group/group_list.html'
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
                user = Group.objects.all()
                for c in user:
                    data.append({'id': int(c.id), 'nombre': str(c.name),
                                 'permisos': [{'id': p.id, 'nombre': p.name} for p in c.permissions.all()]})
                    print(data)
            elif action == 'delete':
                try:
                    id = request.POST['id']
                    if id:
                        ps = User.objects.get(pk=id)
                        ps.delete()
                        data['resp'] = True
                    else:
                        data['error'] = 'Ha ocurrido un error'
                except Exception as e:
                    data['error'] = str(e)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-user-lock'
        data['entidad'] = 'Grupos'
        data['boton'] = 'Nuevo Grupo'
        data['titulo'] = 'Listado de Grupos'
        data['nuevo'] = '/usuario/grupo'
        data['form'] = UserForm
        data['empresa'] = empresa
        return data


class CrudViewGroup(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Group
    template_name = 'front-end/group/group_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            print(action)
            if action == 'add':
                f = GroupForm(request.POST)
                if f.is_valid():
                    f.save()
                    return HttpResponseRedirect('user/groups')
                else:
                    data['form'] = f
                return render(request, 'front-end/group/group_form.html', data)
            elif action == 'delete':
               cli = Group.objects.get(pk=pk)
               cli.delete()
               data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Grupo'
        data['titulo'] = 'Nuevo Grupos'
        data['nuevo'] = '/usuario/newgroup'
        data['form'] = GroupForm
        data['action'] = 'add'
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
