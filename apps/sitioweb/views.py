from django.core.exceptions import ObjectDoesNotExist
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
from apps.sitioweb.forms import SitiowebForm
from apps.sitioweb.models import SitioWeb
from apps.user.models import User
from apps.proveedor.models import Proveedor

opc_icono = 'fa fa-newspaper fa'
opc_entidad = 'Sitio Web'
crud = '/sitio/configurar'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = SitioWeb
    template_name = "front-end/sitio/cliente_list.html"
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
    form_class = SitiowebForm
    template_name = 'front-end/sitio/sitio_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
                web = SitioWeb.objects.first()
                f = SitiowebForm(request.POST, instance=web)
                data = self.save_data(f)
                return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            f = SitiowebForm(request.POST)
            data = self.save_data(f)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            f.save()
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        web = SitioWeb.objects.get(pk=1)
        if SitioWeb.objects.exists():
            data['form'] = SitiowebForm(instance=web)
        else:
            data['form'] = SitiowebForm()
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar'
        data['titulo'] = 'Sitio web'
        data['empresa'] = empresa
        return data


@csrf_exempt
class report(ListView):
    model = Cliente
    template_name = 'front-end/cliente/cliente_report.html'

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
                    data.append([
                        p.id,
                        p.fecha.strftime("%d/%m/%Y"),
                        p.nombres + " " + p.apellidos,
                        p.cedula,
                        p.correo,
                        p.get_sexo_display(),
                        p.direccion,
                        p.telefono
                    ])
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


def sitio(request):
    data = {'empresa': empresa, 'sitio': SitioWeb.objects.first(), 'title': empresa.nombre}
    if request.user.is_authenticated:
        data['group'] = request.user.get_tipo_display
    else:
        data['group'] = 'NONE'
    return render(request,  'front-end/sitio/index.html', data)




