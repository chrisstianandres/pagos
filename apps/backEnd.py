# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import *
from django.http import HttpResponse
from django.http import *
from django.urls import reverse_lazy

from django.views.generic import FormView
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


def signin(request):
    data = {}
    if not request.user.is_authenticated:
        data['title'] = 'Registro de usuario'
        data['nomb'] = nombre_empresa()
        data['form'] = UserForm_online()
        data['crud'] = '/user/new_online'
        data['action'] = 'add'
    else:
        return HttpResponseRedirect("/")
    return render(request, 'front-end/signin.html', data)


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
