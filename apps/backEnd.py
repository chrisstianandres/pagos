from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import *
from django.http import HttpResponse
from django.http import *
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
import json
from django.views.decorators.csrf import csrf_exempt

# -----------------------------------------------PAGINA PRINCIPAL-----------------------------------------------------#
from apps.user.forms import UserForm, UserForm_online
from apps.user.models import User
from apps.empresa.models import Empresa


def nombre_empresa():
    try:
        empresa = Empresa.objects.first()
    except ObjectDoesNotExist:
        empresa = {'nombre': 'Sin nombre'}
    return empresa


def menu(request):
    data = {
        'titulo': 'Menu Principal', 'empresa': nombre_empresa(),
        'icono': 'fas fa-tachometer-alt', 'entidad': 'Menu Principal',
    }
    return render(request, 'front-end/index.html', data)


# -----------------------------------------------LOGEO----------------------------------------------------------------#

def logeo(request):
    data = {}
    if not request.user.is_authenticated:
        data['title'] = 'Inicio de Sesion'
        data['nomb'] = nombre_empresa()
    else:
        return HttpResponseRedirect("/")
    return render(request, 'front-end/login.html', data)


class signin(TemplateView):
    form_class = UserForm_online
    template_name = 'front-end/signin.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = UserForm_online(request.POST, request.FILES)
                if f.is_valid():
                    f.save(commit=False)
                    if verificar(f.data['cedula']):
                        user = f.save()
                        # print(user.id)

                        return HttpResponseRedirect('/login')
                    else:
                        f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                        data['form'] = f
                else:
                    data['title'] = 'Registro de usuario'
                    data['nomb'] = nombre_empresa()
                    data['crud'] = '/signin/'
                    data['action'] = 'add'
                    data['error'] = f.errors
                    data['form'] = f
                    return render(request, 'front-end/signin.html', data)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get(self, request, *args, **kwargs):
        data = {}
        if not self.request.user.is_authenticated:
            data['title'] = 'Registro de usuario'
            data['nomb'] = nombre_empresa()
            data['form'] = UserForm_online()
            data['crud'] = '/signin/'
            data['action'] = 'add'
        else:
            return HttpResponseRedirect("/")
        return render(request, self.template_name, data)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Registro de usuario'
        data['nomb'] = nombre_empresa()
        data['form'] = UserForm_online()
        data['crud'] = '/signin/'
        data['action'] = 'add'
        return data


@csrf_exempt
def connect(request):
    data = {}
    if request.method == 'POST' or None:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.estado == 1:
                login(request, user)
                data['resp'] = True
            else:
                data['error'] = '<strong>Usuario Inactivo </strong>'
        else:
            data['error'] = '<strong>Usuario no valido </strong><br>' \
                            'Verifica las credenciales de acceso y vuelve a intentarlo.'
    else:
        data['error'] = 'Metodo Request no es Valido.'
    return HttpResponse(json.dumps(data), content_type="application/json")


def disconnect(request):
    logout(request)
    return HttpResponseRedirect('/login')


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