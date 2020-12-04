import json
import os
from datetime import datetime

from django.conf import settings
from django.contrib.staticfiles import finders
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from xhtml2pdf import pisa

from apps.backEnd import nombre_empresa
from apps.cliente.forms import ClienteForm
from apps.confeccion.forms import ConfeccionForm, Detalle_confeccionform
from apps.confeccion.models import Confeccion, Detalle_confeccion
from apps.empresa.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.transaccion.forms import TransaccionForm
from apps.transaccion.models import Transaccion

opc_icono = 'fab fa-shirtsinbulk'
opc_entidad = 'Confeccion'
crud = '/confeccion/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Confeccion
    template_name = 'front-end/confeccion/confeccion_list.html'
    permission_required = 'confeccion.view_confeccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'confeccion':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start == '' and end == '':
                    query = Confeccion.objects.filter(transaccion__tipo=3)
                else:
                    query = Confeccion.objects.filter(transaccion__tipo=3, transaccion__fecha_trans__range=[start, end])
                for c in query:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    result = Detalle_confeccion.objects.filter(confeccion_id=id)
                    for p in result:
                        data.append({
                            'producto': p.producto.producto_base.nombre,
                            'categoria': p.producto.producto_base.categoria.nombre,
                            'presentacion': p.producto.producto_base.presentacion.nombre,
                            'cantidad': p.cantidad,
                            'pvp': p.pvp_by_confec,
                            'subtotal': p.subtotal
                        })
            elif action == 'anular':
                id = request.POST['id']
                result = Confeccion.objects.get(id=id)
                result.estado = 2
                result.save()
                data['resp'] = True
            elif action == 'entregar':
                id = request.POST['id']
                result = Confeccion.objects.get(id=id)
                result.estado = 1
                result.fecha_entrega = datetime.now()
                result.save()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Confeccion'
        data['titulo'] = 'Listado de Confecciones'
        data['nuevo'] = '/confeccion/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Confeccion
    template_name = 'front-end/confeccion/confeccion_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                datos = json.loads(request.POST['confeccion'])
                if datos:
                    with transaction.atomic():
                        c = Transaccion()
                        c.fecha_trans = datos['fecha_venta']
                        c.cliente_id = datos['cliente']
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.tipo = 3
                        c.save()
                        v = Confeccion()
                        v.transaccion_id = c.id
                        v.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dv = Detalle_confeccion()
                                dv.confeccion_id = v.id
                                dv.producto_id = int(i['id'])
                                dv.cantidad = int(i['cantidad'])
                                dv.pvp_by_confec = float(i['pvp'])
                                dv.subtotal = float(i['subtotal'])
                                dv.save()
                        data['id'] = v.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Confeccion'
        data['titulo'] = 'Nueva Confeccion'
        data['nuevo'] = '/confeccion/nuevo'
        data['empresa'] = empresa
        data['form'] = TransaccionForm()
        data['formr'] = ConfeccionForm()
        data['form2'] = Detalle_confeccionform()
        data['detalle'] = []
        data['formc'] = ClienteForm()
        return data


class printpdf(View):

    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def pvp_cal(self, *args, **kwargs):
        data = []
        try:
            for i in Detalle_confeccion.objects.filter(confeccion_id=self.kwargs['pk']):
                item = i.confeccion.toJSON()
                item['producto'] = {'producto': i.producto.toJSON()}
                item['pvp'] = format(i.pvp_by_confec, '.2f')
                item['cantidad'] = i.cantidad
                item['subtotal'] = i.subtotal
                data.append(item)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf.html')
            context = {'title': 'Comprobante de Confeccion',
                       'sale': Confeccion.objects.get(pk=self.kwargs['pk']),
                       'det_sale': self.pvp_cal(),
                       'empresa': Empresa.objects.first(),
                       'icon': 'media/imagen.PNG',
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('confeccion:lista'))
