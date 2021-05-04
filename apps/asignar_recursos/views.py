import json

from django.db import transaction
from django.db.models import Count, Q, Sum
from django.http import JsonResponse, HttpResponse
from django.utils.datetime_safe import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.user.models import User
from apps.asignar_recursos.forms import Asig_recursoForm, Detalle_Asig_recursoForm, Detalle_Asig_maquinaForm, \
    NovedadesForm
from apps.asignar_recursos.models import Asig_recurso, Detalle_asig_recurso, Detalle_asig_maquina, Detalle_produccion, \
    Novedades, Detalle_perdidas_materiales
from apps.backEnd import nombre_empresa
from apps.confeccion.models import Confeccion
from apps.maquina.models import Maquina
from apps.material.models import Material
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.models import Producto
from apps.producto_base.models import Producto_base

opc_icono = 'fas fa-toolbox'
opc_entidad = 'Confeccion de Prendas (Produccion)'
crud = '/asignar/crear'
empresa = nombre_empresa()
year = [{'id': y, 'year': (datetime.now().year) - y} for y in range(0, 5)]


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Asig_recurso
    template_name = 'front-end/asignacion/asignacion_list.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Asig_recurso.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start and end:
                    asignacion = Asig_recurso.objects.filter(fecha_asig__range=[start, end])
                else:
                    asignacion = Asig_recurso.objects.all()
                for c in asignacion:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    edit = self.model.objects.get(id=id)
                    for p in edit.detalle_asig_recurso_set.all():
                        item = p.inventario_material.toJSON()
                        item['cant'] = p.cantidad
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_maquina':
                id = request.POST['id']
                if id:
                    data = []
                    for m in Detalle_asig_maquina.objects.filter(asig_recurso_id=id):
                        item = m.toJSON()
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_prendas':
                id = request.POST['id']
                if id:
                    data = []
                    for m in Detalle_produccion.objects.filter(asignacion_id=id):
                        item = m.producto.toJSON()
                        item['cantidad'] = m.cantidad
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_novedades':
                id = request.POST['id']
                if id:
                    data = []
                    for m in Novedades.objects.filter(asig_recurso_id=id):
                        item = m.toJSON()
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_perdidas':
                id = request.POST['id']
                if id:
                    data = []
                    for m in Detalle_perdidas_materiales.objects.filter(det_asignacion__asig_recurso_id=id):
                        item = m.det_asignacion.inventario_material.toJSON()
                        item['cantidad'] = m.cantidad
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'finalizar':
                id = request.POST['id']
                if id:
                    asignar = Asig_recurso.objects.get(id=id)
                    asignar.estado = 2
                    asignar.save()
                    if asignar.detalle_asig_recurso_set.all():
                        for m in Detalle_asig_maquina.objects.filter(asig_recurso_id=id):
                            for x in Maquina.objects.filter(id=m.maquina.pk):
                                x.estado = 0
                                x.save()
                        if Confeccion.objects.get(confeccion_id=asignar.id):
                            pass
                        else:
                            for d in asignar.detalle_produccion_set.all():
                                prd = Producto.objects.get(id=d.producto.id)
                                prd.stock += d.cantidad
                                prd.save()
                    else:
                        data['error'] = 'No ha ingresado insumos a la confeccion'
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Asig_recurso.objects.filter(lote__icontains=term, estado=2, inventariado=0)[0:10]
                for a in query:
                    result = {'id': int(a.id),
                              'text': str('Lote N°: ' + a.lote + ' / Fecha : ' + a.fecha_asig.strftime('%d-%m-%Y'))}
                    data.append(result)
            elif action == 'anular':
                asignar = self.model.objects.get(id=request.POST['id'])
                asignar.estado = 0
                asignar.save()
                if Confeccion.objects.filter(Q(estado=0) | Q(estado=1) | Q(estado=3), confeccion_id=asignar.id):
                    confeccion = Confeccion.objects.get(confeccion_id=asignar.id)
                    confeccion.estado = 2
                    confeccion.save()
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Confeccion'
        data['titulo'] = 'Listado de Confecciones (Produccion)'
        data['nuevo'] = '/asignacion/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Asig_recursoForm
    template_name = 'front-end/produccion/produccion_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                datos = json.loads(request.POST['ingresos'])
                if datos:
                    with transaction.atomic():
                        c = Asig_recurso()
                        c.fecha_asig = datos['fecha_ingreso']
                        c.fecha_fin = datos['fecha_salida']
                        c.user_id = request.user.id
                        c.save()
                        for i in datos['materiales']:
                            dv = Detalle_asig_recurso()
                            dv.asig_recurso_id = c.id
                            dv.inventario_material_id = i['id']
                            dv.cantidad = int(i['cantidad'])
                            dv.ingreso_inicial = int(i['cantidad'])
                            dv.ingreso_actual = int(i['cantidad'])
                            dv.save()
                            s = Material.objects.get(pk=i['id'])
                            s.stock_actual -= int(i['cantidad'])
                            s.save()
                        for m in datos['maquinas']:
                            dm = Detalle_asig_maquina()
                            dm.asig_recurso_id = c.id
                            dm.maquina_id = m['id']
                            dm.save()
                            x = Maquina.objects.get(pk=m['id'])
                            x.estado = 1
                            x.save()
                        for p in datos['productos_estimados']:
                            dtp = Detalle_produccion()
                            dtp.asignacion_id = c.id
                            dtp.producto_id = int(p['id'])
                            dtp.cantidad = int(p['cantidad'])
                            dtp.save()
                            pr = Producto.objects.get(id=int(p['id']))
                            pr.stock += int(p['cantidad'])
                            pr.save()
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
        data['form'] = self.form_class
        data['form_materiales'] = Detalle_Asig_recursoForm()
        data['form_maquinas'] = Detalle_Asig_maquinaForm()
        data['boton'] = 'Guardar Confeccion'
        data['titulo'] = 'Nueva Confeccion'
        data['nuevo'] = '/asignar/nuevo'
        data['empresa'] = empresa
        return data


class Control(ValidatePermissionRequiredMixin, UpdateView):
    form_class = Asig_recursoForm
    model = Asig_recurso
    template_name = 'front-end/produccion/produccion_control.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_data(self):
        data = []
        pk = self.kwargs.get('pk', 0)
        edit = self.model.objects.get(id=pk)
        for p in edit.detalle_asig_recurso_set.all():
            item = p.inventario_material.toJSON()
            item['cant'] = p.cantidad
            item['ingreso_actual'] = p.ingreso_actual
            item['stock_actual'] = p.inventario_material.stock_actual + p.cantidad
            item['id_det'] = p.id
            data.append(item)
        return data

    def get_data_maquina(self):
        data = []
        pk = self.kwargs.get('pk', 0)
        edit = self.model.objects.get(id=pk)
        for p in edit.detalle_asig_maquina_set.all():
            item = p.maquina.toJSON()
            data.append(item)
        return data

    def get_data_perdidas(self):
        data = []
        pk = self.kwargs.get('pk', 0)
        edit = self.model.objects.get(id=pk)
        for det in edit.detalle_asig_recurso_set.all():
            for p in det.detalle_perdidas_materiales_set.all():
                item = p.det_asignacion.inventario_material.toJSON()
                item['cantidad'] = p.cantidad
                item['ingreso_actual'] = p.det_asignacion.ingreso_actual
                item['id_det'] = p.det_asignacion.id
                data.append(item)
        return data

    def get_data_productos(self):
        data = []
        pk = self.kwargs.get('pk', 0)
        edit = self.model.objects.get(id=pk)
        for det in edit.detalle_produccion_set.all():
            item = det.producto.toJSON()
            item['cantidad'] = det.cantidad
            data.append(item)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                datos = json.loads(request.POST['ingresos'])
                if datos:
                    with transaction.atomic():

                        pk = self.kwargs.get('pk', 0)
                        c = self.model.objects.get(id=pk)
                        for m in c.detalle_asig_recurso_set.all():
                            ma = Material.objects.get(id=m.inventario_material.id)
                            ma.stock_actual += m.cantidad
                            ma.save()
                            c.detalle_asig_maquina_set.all().delete()
                        for px in c.detalle_asig_recurso_set.all():
                            for t in Detalle_perdidas_materiales.objects.filter(det_asignacion_id=px.id):
                                t.delete()
                                px.delete()
                                c.detalle_produccion_set.all().delete()
                        for i in datos['materiales']:
                            dv = Detalle_asig_recurso()
                            dv.asig_recurso_id = c.id
                            dv.inventario_material_id = i['id']
                            dv.cantidad = int(i['cant'])
                            dv.ingreso_inicial = int(i['cant'])
                            dv.ingreso_actual = int(i['cant'])
                            dv.save()
                            for p in datos['perdidas']:
                                if p['id'] == i['id']:
                                    dtp = Detalle_perdidas_materiales()
                                    dtp.det_asignacion_id = dv.id
                                    dtp.cantidad = int(p['cantidad'])
                                    dtp.save()
                                    dv.ingreso_actual -= int(p['cantidad'])
                                    dv.save()
                            s = Material.objects.get(pk=i['id'])
                            s.stock_actual -= int(i['cant'])
                            s.save()
                        for m in datos['maquinas']:
                            dm = Detalle_asig_maquina()
                            dm.asig_recurso_id = c.id
                            dm.maquina_id = m['id']
                            dm.save()
                            x = Maquina.objects.get(pk=m['id'])
                            x.estado = 1
                            x.save()
                        if Confeccion.objects.get(confeccion_id=pk):
                            for p in datos['productos']:
                                if c.detalle_produccion_set.filter(producto_id=int(p['id'])):
                                    prod = c.detalle_produccion_set.get(producto_id=int(p['id']))
                                    prod.cantidad = int(p['cantidad'])
                                    prod.save()
                            for pe in datos['productos_eliminados']:
                                if c.detalle_produccion_set.filter(producto_id=int(pe['id'])):
                                    c.detalle_produccion_set.get(producto_id=int(p['id'])).delete()
                        else:
                            for p in datos['productos']:
                                dtp = Detalle_produccion()
                                dtp.asignacion_id = c.id
                                dtp.producto_id = int(p['id'])
                                dtp.cantidad = int(p['cantidad'])
                                dtp.save()
                        data['id'] = c.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'estado_maquina':
                pk = request.POST['id']
                maq = Maquina.objects.get(id=pk)
                maq.estado = 0
                maq.save()
            elif action == 'novedades':
                data = []
                pk = self.kwargs.get('pk', 0)
                nov = Novedades.objects.filter(asig_recurso_id=pk)
                for n in nov:
                    data.append(n.toJSON())
            elif action == 'add_novedad':
                pk = self.kwargs.get('pk', 0)
                novedad = request.POST['novedad']
                nov = Novedades()
                nov.asig_recurso_id = pk
                nov.novedad = novedad
                nov.save()
            elif action == 'edit_novedad':
                pk = request.POST['id']
                novedad = request.POST['novedad']
                fecha = request.POST['fecha']
                nov = Novedades.objects.get(id=pk)
                nov.novedad = novedad
                nov.fecha = fecha
                nov.save()
            elif action == 'del_novedad':
                pk = request.POST['id']
                nov = Novedades.objects.get(id=pk)
                nov.delete()
            elif action == 'del_novedad_all':
                pk = self.kwargs.get('pk', 0)
                edit = self.model.objects.get(id=pk)
                edit.novedades_set.all().delete()
            elif action == 'get_det_asig':
                data = []
                pk = self.kwargs.get('pk', 0)
                edit = self.model.objects.get(id=pk)
                ids = json.loads(request.POST['ids'])
                print(edit.detalle_asig_recurso_set.all().query)
                for p in edit.detalle_asig_recurso_set.all().exclude(id__in=ids):
                    item = p.inventario_material.toJSON()
                    item['cantidad'] = 1
                    item['ingreso_actual'] = p.ingreso_actual
                    item['maximo'] = p.cantidad
                    data.append(item)
            # elif action == 'refresh_perd':
            #     data = []
            #     pk = request.POST['id']
            #     edit = Detalle_asig_recurso.objects.get(id=pk)
            #     edit.ingreso_actual = edit.cantidad
            #     edit.save()
            #     per = Detalle_perdidas_materiales.objects.get(det_asignacion_id=pk)
            #     per.delete()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        edit = self.model.objects.get(id=pk)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['form'] = self.form_class(instance=edit)
        data['inicio'] = edit.fecha_asig.strftime('%Y/%m/%d')
        data['fin'] = edit.fecha_fin.strftime('%Y/%m/%d')
        data['materiales'] = self.get_data()
        data['maquinas'] = self.get_data_maquina()
        data['perdidas'] = self.get_data_perdidas()
        data['productos'] = self.get_data_productos()
        data['form_novedades'] = NovedadesForm()
        data['form_materiales'] = Detalle_Asig_recursoForm()
        data['form_maquinas'] = Detalle_Asig_maquinaForm()
        data['boton'] = 'Guardar'
        data['titulo'] = 'Control Confeccion'
        data['empresa'] = empresa
        return data


class PerdidasView(ValidatePermissionRequiredMixin, ListView):
    template_name = 'front-end/produccion/perdidas_list.html'
    model = Detalle_perdidas_materiales

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start and end:
                    perdida = self.model.objects.values('det_asignacion__inventario_material_id')\
                        .filter(det_asignacion__asig_recurso__fecha_asig__range=[start, end])\
                        .annotate(Sum('cantidad')).order_by()

                else:
                    perdida = self.model.objects.values('det_asignacion__inventario_material_id').\
                        annotate(Sum('cantidad')).order_by()
                for c in perdida:
                    mat = Material.objects.get(id=c['det_asignacion__inventario_material_id'])
                    data.append([
                        mat.producto_base.nombre,
                        mat.producto_base.categoria.nombre,
                        mat.get_calidad_display(),
                        mat.color.nombre,
                        mat.tipo_material.nombre,
                        mat.get_unidad_medida_display(),
                        c['cantidad__sum']
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Reporte de Perdidas de materiales'
        data['titulo'] = 'Reporte de Perdidas de materiales'
        data['empresa'] = empresa
        data['year'] = year
        return data


class ProdClienteView(ValidatePermissionRequiredMixin, ListView):
    template_name = 'front-end/produccion/report_by_cliente_list.html'
    model = Asig_recurso

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                cliente = request.POST['cliente']
                data = []
                if cliente:
                    det = Asig_recurso.objects.filter(user__tipo=0, user_id=cliente, estado=2)
                    for a in det:
                        for d in Detalle_produccion.objects.filter(asignacion_id=a.id):
                            data.append([
                                d.asignacion.id,
                                d.asignacion.fecha_fin,
                                d.producto.producto_base.nombre,
                                d.producto.producto_base.categoria.nombre,
                                d.producto.color.nombre,
                                d.producto.talla.talla_full(),
                                d.cantidad
                            ])
                else:
                    data = []
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-user'
        data['entidad'] = 'Reporte de Produccion por cliente'
        data['titulo'] = 'Reporte de Produccion por cliente'
        data['empresa'] = empresa
        data['year'] = year
        return data


class ProdPrendaView(ValidatePermissionRequiredMixin, ListView):
    template_name = 'front-end/produccion/report_by_prenda_list.html'
    model = Asig_recurso

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                prenda = request.POST['prenda']
                data = []
                if prenda == '0':
                    det = Asig_recurso.objects.filter(estado=2)
                    for a in det:
                        for d in Detalle_produccion.objects.filter(asignacion_id=a.id):
                            data.append([
                                d.asignacion.id,
                                d.asignacion.fecha_fin,
                                d.producto.producto_base.nombre,
                                d.producto.producto_base.categoria.nombre,
                                d.producto.color.nombre,
                                d.producto.talla.talla_full(),
                                d.cantidad
                            ])
                elif prenda:
                    det = Asig_recurso.objects.filter(estado=2)
                    for a in det:
                        for d in Detalle_produccion.objects.filter(asignacion_id=a.id, producto_id=prenda):
                            data.append([
                                d.asignacion.id,
                                d.asignacion.fecha_fin,
                                d.producto.producto_base.nombre,
                                d.producto.producto_base.categoria.nombre,
                                d.producto.color.nombre,
                                d.producto.talla.talla_full(),
                                d.cantidad
                            ])
                else:
                    data = []
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Producto.objects.filter(producto_base__nombre__icontains=term)
                for a in query:
                    result = {'id': int(a.id),
                              'text': str(str(a.producto_base.nombre) + ' / ' + str(a.color.nombre) + ' / ' + str(
                                  a.talla.talla_full()))}
                    data.append(result)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-tshirt'
        data['entidad'] = 'Reporte de Produccion por prenda'
        data['titulo'] = 'Reporte de Produccion por prenda'
        data['empresa'] = empresa
        data['year'] = year
        return data


class reportView(ValidatePermissionRequiredMixin, ListView):
    template_name = 'front-end/asignacion/asignacion_report.html'
    model = Asig_recurso

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start and end:
                    det = Asig_recurso.objects.all()
                    for a in det:
                        for d in Detalle_produccion.objects.filter(asignacion_id=a.id,
                                                                   asignacion__fecha_asig__range=[start, end]):
                            data.append([
                                d.asignacion.id,
                                d.asignacion.fecha_fin,
                                d.producto.producto_base.nombre,
                                d.producto.producto_base.categoria.nombre,
                                d.producto.color.nombre,
                                d.producto.talla.talla_full(),
                                d.cantidad
                            ])
                else:
                    det = Asig_recurso.objects.all()
                    for a in det:
                        for d in Detalle_produccion.objects.filter(asignacion_id=a.id):
                            data.append([
                                d.asignacion.id,
                                d.asignacion.fecha_fin,
                                d.producto.producto_base.nombre,
                                d.producto.producto_base.categoria.nombre,
                                d.producto.color.nombre,
                                d.producto.talla.talla_full(),
                                d.cantidad
                            ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-calendar'
        data['entidad'] = 'Reporte de Produccion por fechas'
        data['titulo'] = 'Reporte de Produccion por fechas'
        data['empresa'] = empresa
        data['year'] = year
        return data


