import json
from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.compra.forms import CompraForm, Detalle_CompraForm
from apps.compra.models import Compra, Detalle_compra
from apps.empresa.models import Empresa
from apps.inventario_material.models import Inventario_material
from apps.material.models import Material
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.models import Producto
from datetime import date
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from apps.producto_base.models import Producto_base
from apps.proveedor.forms import ProveedorForm

opc_icono = 'fa fa-shopping-bag'
opc_entidad = 'Compras'
crud = '/compra/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Compra
    template_name = 'front-end/compra/compra_list.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Compra.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            start = request.POST['start_date']
            end = request.POST['end_date']
            if action == 'list':
                data = []
                if start and end:
                    compra = Compra.objects.filter(fecha_compra__range=[start, end])
                else:
                    compra = Compra.objects.all()
                for c in compra:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    for p in Detalle_compra.objects.all():
                        item = p.toJSON()
                        item['p_compra'] = float((p.p_compra_actual * 100) / (100 + 12))
                        item['subtotal'] = float(p.subtotal)
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Compra'
        data['titulo'] = 'Listado de Compras'
        data['nuevo'] = '/compra/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Compra
    template_name = 'front-end/compra/compra_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        pk = request.POST['id']
        try:
            if action == 'add':
                datos = json.loads(request.POST['compras'])
                if datos:
                    pr = []
                    with transaction.atomic():
                        c = Compra()
                        c.fecha_compra = datos['fecha_compra']
                        c.proveedor_id = datos['proveedor']
                        c.user_id = request.user.id
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.save()
                        for i in datos['productos']:
                            dv = Detalle_compra()
                            dv.compra_id = c.id
                            dv.material_id = i['id']
                            dv.cantidad = int(i['cantidad'])
                            dv.subtotal = float(i['subtotal'])
                            x = Material.objects.get(pk=i['id'])
                            dv.p_compra_actual = float(x.p_compra)
                            pb = Producto_base.objects.get(material=x.id)
                            pb.stock = pb.stock + int(i['cantidad'])
                            pb.save()
                            x.save()
                            dv.save()
                            for p in range(0, i['cantidad']):
                                inv = Inventario_material()
                                inv.compra_id = c.id
                                inv.material_id = x.id
                                inv.save()
                        data['id'] = c.id
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
        data['boton'] = 'Guardar Compra'
        data['titulo'] = 'Nueva Compra'
        data['nuevo'] = '/compra/nuevo'
        data['empresa'] = empresa
        data['form'] = CompraForm()
        data['form2'] = Detalle_CompraForm()
        data['detalle'] = []
        data['formp'] = ProveedorForm()
        return data



@csrf_exempt
def data(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            compra = Compra.objects.all()
            for c in compra:
                data.append([
                    c.fecha_compra.strftime('%d-%m-%Y'),
                    c.proveedor.nombres,
                    c.empleado.get_full_name(),
                    format(c.total, '.2f'),
                    c.id,
                    c.get_estado_display(),
                    c.id
                ])
        else:
            compra = Compra.objects.filter(fecha_compra__range=[start_date, end_date])
            for c in compra:
                data.append([
                    c.fecha_compra.strftime('%d-%m-%Y'),
                    c.proveedor.nombres,
                    c.empleado.get_full_name(),
                    format(c.total, '.2f'),
                    c.id,
                    c.get_estado_display(),
                    c.id
                ])
    except:
        pass
    return JsonResponse(data, safe=False)


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../compra/get_producto', 'empresa': empresa,
        'boton': 'Guardar Compra', 'action': 'add', 'titulo': 'Nueva Compra',
        'key': ''
    }
    if request.method == 'GET':
        data['form'] = CompraForm()
        data['form2'] = Detalle_CompraForm()
        data['detalle'] = []
        data['formp'] = ProveedorForm()
    return render(request, 'front-end/compra/compra_form.html', data)


@csrf_exempt
def crear(request):
    data = {}
    if request.method == 'POST':
        datos = json.loads(request.POST['compras'])
        if datos:
            pr = []
            with transaction.atomic():
                c = Compra()
                c.fecha_compra = datos['fecha_compra']
                c.proveedor_id = datos['proveedor']
                c.empleado_id = request.user.id
                c.subtotal = float(datos['subtotal'])
                c.iva = float(datos['iva'])
                c.total = float(datos['total'])
                c.save()
                for i in datos['productos']:
                    dv = Detalle_compra()
                    dv.compra_id = c.id
                    dv.producto_id = i['id']
                    dv.cantidad = int(i['cantidad'])
                    dv.subtotal = float(i['subtotal'])
                    x = Producto.objects.get(pk=i['id'])
                    x.stock = x.stock + int(i['cantidad'])
                    dv.p_compra_actual = float(x.p_compra)
                    x.save()
                    dv.save()
                    for p in range(0, i['cantidad']):
                        item = c.toJSON()
                        item['producto'] = x.toJSON()
                        item['serie'] = 0
                        item['fecha_salida'] = ''
                        item['estado'] = 1
                        pr.append(item)
                data['productos'] = pr
                data['id'] = c.id
                data['resp'] = True
        else:
            data['resp'] = False
            data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")


def editar(request, id):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../../compra/get_producto', 'empresa': empresa,
        'boton': 'Editar Compra', 'action': 'edit', 'titulo': 'Editar Registro de una Compra',
        'key': id
    }
    compra = Compra.objects.get(id=id)
    if request.method == 'GET':
        data['form'] = CompraForm(instance=compra)
        data['form2'] = Detalle_CompraForm()
        data['detalle'] = json.dumps(get_detalle_productos(id))
    return render(request, 'front-end/compra/compra_form.html', data)


@csrf_exempt
def editar_save(request):
    data = {}
    datos = json.loads(request.POST['compras'])
    if request.POST['action'] == 'edit':
        with transaction.atomic():
            c = Compra.objects.get(pk=request.POST['key'])
            c.fecha_compra = datos['fecha_compra']
            c.proveedor_id = datos['proveedor']
            c.subtotal = float(datos['subtotal'])
            c.iva = float(datos['iva'])
            c.total = float(datos['total'])
            c.save()
            c.detalle_compra_set.all().delete()
            for i in datos['insumos']:
                dv = Detalle_compra()
                dv.compra_id = c.id
                dv.insumo_id = i['id']
                dv.cantidad = int(i['cantidad'])
                dv.save()
                data['resp'] = True
    else:
        data['resp'] = False
        data['error'] = "Datos Incompletos"
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_detalle_productos(id):
    data = []
    try:
        for i in Detalle_compra.objects.filter(compra_id=id):
            iva_emp = Empresa.objects.get(pk=1)
            item = i.producto.toJSON()
            item['cantidad'] = i.cantidad
            item['iva_emp'] = format(iva_emp.iva, '.2f')
            data.append(item)
    except:
        pass
    return data


@csrf_exempt
def get_producto(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            producto = Producto.objects.filter(pk=id)
            iva_emp = Empresa.objects.get(pk=1)
            data = []
            for i in producto:
                item = i.toJSON()
                item['cantidad'] = 1
                item['subtotal'] = 0.00
                item['iva_emp'] = iva_emp.iva
                cal = float(item['p_compra']) / (item['iva_emp'] + 100)
                item['p_compra'] = cal
                data.append(item)
        else:
            data['error'] = 'No ha selecionado ningun Insumo'
    except Exception as e:
        data['error'] = 'Ha ocurrido un error'
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_detalle(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            data = []
            for p in Detalle_compra.objects.filter(compra_id=id):
                item = p.toJSON()
                item['p_compra'] = float((p.p_compra_actual*100)/(100+empresa.iva))
                item['subtotal'] = float(p.compra.subtotal)
                data.append(item)
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


@csrf_exempt
def estado(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            with transaction.atomic():
                es = Compra.objects.get(pk=id)
                es.estado = 0
                for i in Inventario.objects.filter(compra_id=id):
                    ch = Producto.objects.get(id=i.producto.id)
                    if i.venta != None:
                        data['error'] = 'No se puede devolver esta compra porque los productos ya fueron vendidos'
                        data['content'] = 'Prueba con otra venta'
                    else:
                        for d in Detalle_compra.objects.filter(compra_id=id):
                            ch.stock = int(ch.stock) - int(d.cantidad)
                        i.delete()
                        es.save()
                        ch.save()
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            es = Compra.objects.get(id=id)
            es.delete()
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


@csrf_exempt
def index(request):
    data = {}
    try:
        data = []
        h = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)
        for p in Detalle_compra.objects.filter(compra__fecha_compra__range=[h, h + timedelta(days=6)],
                                               compra__estado=1):
            data.append(p.toJSON())
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


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
            iva_emp = Empresa.objects.get(pk=1)
            for i in Detalle_compra.objects.filter(compra_id=self.kwargs['pk']):
                item = i.compra.toJSON()
                item['producto'] = i.producto.toJSON()
                item['pvp'] = format(((i.p_compra_actual * 100) / (iva_emp.iva + 100)), '.2f')
                item['cantidad'] = i.cantidad
                item['subtotal'] = format(i.subtotal, '.2f')
                data.append(item)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf_compra.html')
            context = {'title': 'Comprobante de Compra',
                       'sale': Compra.objects.get(pk=self.kwargs['pk']),
                       'det_sale': self.pvp_cal(),
                       'empresa': Empresa.objects.get(id=1),
                       'icon': 'media/logo_don_chuta.png'
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('compra:lista'))


@csrf_exempt
def data_report(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            query = Detalle_compra.objects.values('compra__fecha_compra', 'producto__nombre',
                                                 'p_compra_actual').order_by().annotate(Sum('cantidad'))
            for p in query:
                data.append([
                    p['compra__fecha_compra'].strftime("%d/%m/%Y"),
                    p['producto__nombre'],
                    int(p['cantidad__sum']),
                    format(p['p_compra_actual'], '.2f'),
                    format(p['p_compra_actual'] * p['cantidad__sum'], '.2f'),
                ])

        else:
            query = Detalle_compra.objects.values('compra__fecha_compra', 'producto__nombre', 'producto__pvp') \
                .filter(compra__fecha_compra__range=[start_date, end_date]).order_by().annotate(Sum('cantidad'))
            for p in query:
                data.append([
                    p['compra__fecha_compra'].strftime("%d/%m/%Y"),
                    p['producto__nombre'],
                    int(p['cantidad__sum']),
                    format(p['producto__pvp'], '.2f'),
                    format(p['producto__pvp'] * p['cantidad__sum'], '.2f'),
                ])
    except:
        pass
    return JsonResponse(data, safe=False)


class report(ListView):
    model = Compra
    template_name = 'front-end/compra/compra_report_product.html'

    def get_queryset(self):
        return Compra.objects.none()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Compra'
        data['titulo'] = 'Reporte de Compras'
        data['nuevo'] = '/compra/nuevo'
        data['empresa'] = empresa
        data['filter_prod'] = '/compra/report_total'
        return data


@csrf_exempt
def data_report_total(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    try:
        if start_date == '' and end_date == '':
            query = Compra.objects.values('fecha_compra', 'proveedor__nombres', 'empleado__first_name',
                                          'empleado__last_name').order_by().annotate(Sum('total'))
            for p in query:
                data.append([
                    p['fecha_compra'].strftime("%d/%m/%Y"),
                    p['proveedor__nombres'],
                    p['empleado__first_name'] + " " + p['empleado__last_name'],
                    format(p['total__sum'], '.2f')
                ])
        else:
            query = Compra.objects.values('fecha_compra', 'proveedor__nombres', 'empleado__first_name',
                                          'empleado__last_name', 'total').filter(
                fecha_compra__range=[start_date, end_date])
            for p in query:
                data.append([
                    p['fecha_compra'].strftime("%d/%m/%Y"),
                    p['proveedor__nombres'],
                    p['empleado__first_name'] + " " + p['empleado__last_name'],
                    format(p['total'], '.2f')
                ])
    except:
        pass
    return JsonResponse(data, safe=False)


class report_total(ListView):
    model = Compra
    template_name = 'front-end/compra/compra_report_total.html'

    def get_queryset(self):
        return Compra.objects.none()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Compra'
        data['titulo'] = 'Reporte de Compras Totales'
        data['nuevo'] = '/compra/nuevo'
        data['empresa'] = empresa
        data['filter_prod'] = '/compra/report_by_product'
        return data
