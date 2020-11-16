from django.shortcuts import render

from apps.empresa.forms import EmpresaForm
from apps.empresa.models import Empresa

opc_icono = 'fa fa-cogs'
opc_entidad = 'Configuracion'
crud = '/empresa/configuracion/'


def editar(request):
    config = Empresa.objects.get(id=1)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa': config,
        'boton': 'Editar', 'titulo': 'Configuracion', 'form': EmpresaForm(instance=config)
    }
    if request.method == 'GET':
        f = EmpresaForm(instance=config)
    else:
        f = EmpresaForm(request.POST, instance=config)
        if f.is_valid():
            f.save()
            data['form'] = f
        else:
            data['form'] = f
        return render(request, 'front-end/empresa/empresa_form.html', data)
    data['form'] = f
    return render(request, 'front-end/empresa/empresa_form.html', data)