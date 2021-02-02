import json

from django.db import transaction
from django.db.models import Count, Subquery, Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.asignar_recursos.forms import Asig_recursoForm, Detalle_Asig_recursoForm, Detalle_Asig_maquinaForm
from apps.asignar_recursos.models import Detalle_asig_recurso, Detalle_asig_maquina
from apps.backEnd import nombre_empresa
from apps.empresa.models import Empresa
from apps.inventario_material.models import Inventario_material
from apps.inventario_productos.models import Inventario_producto
from apps.maquina.models import Tipo_maquina
from apps.mixins import ValidatePermissionRequiredMixin
from apps.produccion.forms import *
from apps.produccion.models import Produccion, Detalle_perdidas_materiales, Detalle_perdidas_productos, \
    Detalle_produccion
from apps.producto_base.models import Producto_base

opc_icono = 'fas fa-toolbox'
opc_entidad = 'Produccion'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Produccion
    template_name = 'front-end/produccion/produccion_list.html'
    permission_required = 'produccion.view_produccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Produccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start and end:
                    produccion = Produccion.objects.filter(fecha_ingreso__range=[start, end])
                else:
                    produccion = Produccion.objects.all()
                for c in produccion:
                    data.append(c.toJSON())
            elif action == 'detalle_materiales':
                id = request.POST['id']
                if id:
                    data = []
                    prod = Produccion.objects.get(id=id)
                    asig = Asig_recurso.objects.get(id=prod.asignacion_id)
                    det = Detalle_asig_recurso.objects.filter(asig_recurso_id=asig.id).values('inventario_material__material_id').annotate(
                        total=Count('inventario_material__material_id')). \
                        order_by('-total')
                    for p in det:
                        px = Material.objects.get(id=int(p['inventario_material__material_id']))
                        item = px.toJSON()
                        item['total'] = int(p['total'])
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_maquinas':
                id = request.POST['id']
                if id:
                    data = []
                    prod = Produccion.objects.get(id=id)
                    asig = Asig_recurso.objects.get(id=prod.asignacion_id)
                    det = Detalle_asig_maquina.objects.filter(asig_recurso_id=asig.id)
                    for p in det:
                        item = p.toJSON()
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_estimados':
                id = request.POST['id']
                if id:
                    data = []
                    det = Detalle_produccion.objects.filter(produccion_id=id)
                    for p in det:
                        px = Producto.objects.get(id=p.producto.id)
                        item = px.toJSON()
                        item['cantidad'] = int(p.cantidad)
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    producto = Inventario_producto.objects.filter(produccion__produccion_id=id).values('produccion__producto_id').annotate(
                        total=Count('id')). \
                        order_by('-total')
                    for p in producto:
                        px = Producto.objects.get(id=int(p['produccion__producto_id']))
                        item = px.toJSON()
                        item['total'] = int(p['total'])
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_perdidas_materiales':
                id = request.POST['id']
                if id:
                    data = []
                    material = Detalle_perdidas_materiales.objects.filter(produccion_id=id)
                    for m in material:
                        item = m.toJSON()
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'detalle_perdidas_productos':
                id = request.POST['id']
                if id:
                    data = []
                    producto = Detalle_perdidas_productos.objects.filter(produccion__produccion_id=id)
                    for m in producto:
                        px = Producto.objects.get(id=int(m.produccion.producto.id))
                        item = px.toJSON()
                        item['total'] = int(m.cantidad)
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'delete':
                id = request.POST['id']
                dtpm = Detalle_perdidas_materiales.objects.filter(produccion_id=id)
                invp = Inventario_producto.objects.filter(produccion_id=id)
                dtpp = Detalle_perdidas_productos.objects.filter(produccion_id=id)
                for a in dtpm:
                    a.delete()
                for b in invp:
                    b.delete()
                for c in dtpp:
                    c.delete()
                pr = Produccion.objects.get(id=id)
                asg = Asig_recurso.objects.get(id=pr.asignacion_id)
                asg.inventariado = 0
                asg.save()
                pr.estado = 1
                pr.save()
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Registro de Produccion'
        data['titulo'] = 'Listado de registros de Produccion'
        data['nuevo'] = '/produccion/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Produccion
    template_name = 'front-end/produccion/produccion_form.html'
    permission_required = 'produccion.add_produccion'

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
                        a = Asig_recurso()
                        a.fecha_asig = datos['fecha_ingreso']
                        a.lote = datos['lote']
                        a.user_id = request.user.id
                        a.save()
                        c = Produccion()
                        c.novedades = datos['novedades']
                        c.asignacion_id = a.id
                        c.save()
                        for i in datos['materiales']:
                            for inv in Inventario_material.objects.filter(material_id=i['id'], estado=1)[:i['cantidad']]:
                                dv = Detalle_asig_recurso()
                                dv.asig_recurso_id = c.id
                                dv.inventario_material_id = inv.id
                                inv.estado = 0
                                inv.save()
                                dv.save()
                            s = Material.objects.get(pk=i['id'])
                            stock = int(Inventario_material.objects.filter(material_id=i['id'], estado=1).count())
                            s.stock = stock
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
                            dtp.produccion_id = c.id
                            dtp.producto_id = p['id']
                            dtp.cantidad = int(p['cantidad'])
                            dtp.save()
                        data['id'] = c.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'agg_more':
                datos = json.loads(request.POST['ingresos'])
                if datos:
                    with transaction.atomic():
                        a = Asig_recurso.objects.get(lote=datos['lote'])
                        for i in datos['materiales']:
                            for inv in Inventario_material.objects.filter(material_id=i['id'], estado=1)[:i['cantidad']]:
                                dv = Detalle_asig_recurso()
                                dv.asig_recurso_id = a.id
                                dv.inventario_material_id = inv.id
                                inv.estado = 0
                                inv.save()
                                dv.save()
                            s = Material.objects.get(pk=i['id'])
                            stock = int(Inventario_material.objects.filter(material_id=i['id'], estado=1).count())
                            s.stock = stock
                            s.save()
                        for m in datos['maquinas']:
                            dm = Detalle_asig_maquina()
                            dm.asig_recurso_id = a.id
                            dm.maquina_id = m['id']
                            dm.save()
                            x = Maquina.objects.get(pk=m['id'])
                            x.estado = 1
                            x.save()
                        for p in datos['productos_estimados']:
                            dtp = Detalle_produccion()
                            dtp.produccion_id = a.id
                            dtp.producto_id = p['id']
                            dtp.cantidad = int(p['cantidad'])
                            dtp.save()
                        data['id'] = a.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'finalizar':
                datos = json.loads(request.POST['ingresos'])
                if datos:
                    with transaction.atomic():
                        lote = datos['lote']
                        asig = Asig_recurso.objects.get(lote=lote)
                        asig.inventariado = 1
                        c = Produccion.objects.get(id=asig.id)
                        c.estado = 0
                        c.save()
                        dtmq = Detalle_asig_maquina.objects.filter(asig_recurso_id=asig.id)
                        for m in dtmq:
                            maq = Maquina.objects.get(id=m.id)
                            maq.estado=0
                            maq.save()
                        asig.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                if i['cantidad'] >= 1:
                                    for p in range(0, i['cantidad']):
                                        dtp = Detalle_produccion.objects.get(produccion_id=c.id, producto_id=int(i['id']))
                                        dv = Inventario_producto()
                                        dv.produccion_id = dtp.id
                                        dv.save()
                                    st = Inventario_producto.objects.filter(produccion__producto_id=int(i['id']), estado=1).count()
                                    pp = Producto.objects.get(id=int(i['id']))
                                    pp.stock = int(st)
                                    pp.save()
                        if datos['perdidas_productos']:
                            for m in datos['perdidas_productos']:
                                if m['perdida'] >= 1:
                                    dtp = Detalle_produccion.objects.get(produccion_id=c.id, producto_id=int(i['id']))
                                    dm = Detalle_perdidas_productos()
                                    dm.produccion_id = dtp.id
                                    dm.cantidad = m['perdida']
                                    dm.save()
                        if datos['perdidas_materiales']:
                            for p in datos['perdidas_materiales']:
                                dp = Detalle_perdidas_materiales()
                                dp.produccion_id = c.id
                                dp.material_id = p['id']
                                dp.cantidad = p['cantidad']
                                dp.save()
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
        data['boton'] = 'Guardar Produccion'
        data['titulo'] = 'Nuevo Registro de produccion Produccion'
        data['nuevo'] = '/produccion/nuevo'
        data['empresa'] = empresa
        data['form'] = ProduccionForm()
        data['form_asig'] = Asig_recursoForm()
        data['form_materiales'] = Detalle_Asig_recursoForm()
        data['detalle_materiales'] = []
        data['form_maquinas'] = Detalle_Asig_maquinaForm()
        data['form4'] = Detalle_perdidas_materialesForm()
        data['detalle'] = []
        return data


class report_total(ValidatePermissionRequiredMixin, ListView):
    model = Produccion
    template_name = 'front-end/produccion/produccion_report.html'
    permission_required = 'produccion.view_produccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Produccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Inventario_producto.objects.values('produccion__produccion__fecha_ingreso',
                                                               'produccion__produccion__novedades',
                                                               'produccion__produccion__asignacion__lote').filter(
                        produccion__produccion__estado=0) \
                        .order_by().annotate(Count('produccion__produccion__asignacion__lote'))

                else:
                    query = Inventario_producto.objects.values('produccion__produccion__fecha_ingreso',
                                                               'produccion__produccion__novedades',
                                                               'produccion__produccion__asignacion__lote') \
                        .filter(produccion__produccion__fecha_ingreso__range=[start_date, end_date],
                                produccion__produccion__estado=0).order_by().annotate(
                        Count('produccion__produccion__asignacion__lote'))

                for p in query:
                    data.append([
                        p['produccion__produccion__fecha_ingreso'].strftime("%d/%m/%Y"),
                        p['produccion__produccion__asignacion__lote'],
                        p['produccion__produccion__novedades'],
                        int(p['produccion__produccion__asignacion__lote__count'])
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Produccion'
        data['titulo'] = 'Reporte de produccion'
        data['empresa'] = empresa
        return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Produccion
    template_name = 'front-end/produccion/produccion_report_product.html'
    permission_required = 'produccion.view_produccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Produccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Inventario_producto.objects.values('produccion__produccion__fecha_ingreso',
                                                               'produccion__produccion__asignacion__lote',
                                                               'produccion__producto_id').filter(
                        produccion__produccion__estado=0) \
                        .order_by().annotate(Count('id'))
                else:
                    query = Inventario_producto.objects.values('produccion__produccion__fecha_ingreso',
                                                               'produccion__produccion__asignacion__lote',
                                                               'produccion__producto_id') \
                        .filter(produccion__produccion__fecha_ingreso__range=[start_date, end_date],
                                produccion__produccion__estado=0).order_by().annotate(
                        Count('id'))
                for p in query:
                    pr = Producto.objects.get(id=int(p['produccion__producto_id']))
                    data.append([
                        p['produccion__produccion__fecha_ingreso'].strftime("%d/%m/%Y"),
                        pr.producto_base.nombre,
                        pr.producto_base.categoria.nombre,
                        pr.presentacion.nombre,
                        p['produccion__produccion__asignacion__lote'],
                        int(p['id__count']),
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Produccion por Producto'
        data['empresa'] = empresa
        return data


class report_perdida(ValidatePermissionRequiredMixin, ListView):
    model = Produccion
    template_name = 'front-end/produccion/produccion_report_product_perdido.html'
    permission_required = 'produccion.view_produccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Produccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Detalle_perdidas_productos.objects.values('produccion__produccion__fecha_ingreso',
                                                                      'produccion__produccion__asignacion__lote',
                                                                      'produccion__producto_id').filter(
                        # producto__producto_base_id
                        produccion__produccion__estado=0) \
                        .order_by().annotate(Count('id'))
                else:
                    query = Detalle_perdidas_productos.objects.values('produccion__produccion__fecha_ingreso',
                                                                      'produccion__produccion__asignacion__lote',
                                                                      'produccion__producto_id') \
                        .filter(produccion__produccion__fecha_ingreso__range=[start_date, end_date],
                                produccion__produccion__estado=0).order_by().annotate(
                        Count('id'))
                for p in query:
                    pr = Producto.objects.get(id=int(p['produccion__producto_id']))
                    data.append([
                        p['produccion__produccion__fecha_ingreso'].strftime("%d/%m/%Y"),
                        pr.producto_base.nombre,
                        pr.producto_base.categoria.nombre,
                        pr.presentacion.nombre,
                        p['produccion__produccion__asignacion__lote'],
                        int(p['id__count']),
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fas fa-book-dead'
        data['entidad'] = 'Perdidas en productos'
        data['titulo'] = 'Reporte de Productos Perdido '
        data['empresa'] = empresa
        return data


class report_perdida_materiales(ValidatePermissionRequiredMixin, ListView):
    model = Produccion
    template_name = 'front-end/produccion/produccion_report_material_perdido.html'
    permission_required = 'produccion.view_produccion'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Produccion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            print(action)
            if action == 'report':
                if start_date == '' and end_date == '':
                    query = Detalle_perdidas_materiales.objects.values('produccion__fecha_ingreso',
                                                                       'produccion__asignacion__lote',
                                                                       'material_id').filter(
                        produccion__estado=0) \
                        .order_by().annotate(Count('id'))
                else:
                    query = Detalle_perdidas_materiales.objects.values('produccion__fecha_ingreso',
                                                                       'produccion__asignacion__lote',
                                                                       'material_id') \
                        .filter(produccion__fecha_ingreso__range=[start_date, end_date],
                                produccion__estado=0).order_by().annotate(
                        Count('id'))
                for p in query:
                    pr = Material.objects.get(id=int(p['material_id']))
                    data.append([
                        p['produccion__fecha_ingreso'].strftime("%d/%m/%Y"),
                        pr.producto_base.nombre,
                        pr.producto_base.categoria.nombre,
                        pr.calidad,
                        '{} / {}'.format(pr.medida, pr.ud_medida),
                        pr.tipo_material.nombre,
                        pr.producto_base.descripcion,
                        p['produccion__asignacion__lote'],
                        int(p['id__count']),
                    ])
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fas fa-book-dead'
        data['entidad'] = 'Perdidas en Materiales'
        data['titulo'] = 'Reporte de Materiales Perdidos '
        data['empresa'] = empresa
        return data


@csrf_exempt
def edit(request, id):
    data = {}
    produccion = Produccion.objects.get(id=id)
    asig = Asig_recurso.objects.get(id=produccion.id)
    data['titulo'] = 'Ingreso de materiales'
    data['icono'] = opc_icono
    data['entidad'] = opc_entidad
    data['boton'] = 'Guardar Produccion'
    data['form'] = ProduccionForm(instance=produccion)
    data['form_asig'] = Asig_recursoForm(instance=asig)
    data['form_materiales'] = Detalle_Asig_recursoForm()
    data['action'] = 'agg_more'
    # for d in Detalle_asig_recurso.objects\
    #         .values('inventario_material__material__producto_base_id').filter(asig_recurso_id=asig.id).annotate(cantidad=Count('id')):
    #     mat = Material.objects.get(producto_base_id=d['inventario_material__material__producto_base_id'])
    #     array = mat.toJSON()
    #     array['cantidad'] = d['cantidad']
    #     materiales.append(array)
    # for m in Detalle_asig_maquina.objects.filter(asig_recurso_id=asig.id):
    #     maquinas.append(m.maquina.toJSON())
    # print(maquinas)
    # # data = {'materiales': materiales, 'maquinas': maquinas}
    # data['materiales'] =materiales
    # data['maquinas'] =maquinas
    return render(request, 'front-end/produccion/produccion_form.html', data)


@csrf_exempt
def finalizar(request, id):
    data = {}
    productos = []
    materiales = []
    produccion = Produccion.objects.get(id=id)
    asig = Asig_recurso.objects.get(id=produccion.id)
    data['titulo'] = 'Ingreso de materiales'
    data['icono'] = opc_icono
    data['entidad'] = opc_entidad
    data['boton'] = 'Guardar Produccion'
    data['form'] = ProduccionForm(instance=produccion)
    data['form_asig'] = Asig_recursoForm(instance=asig)
    data['form_materiales'] = Detalle_Asig_recursoForm()
    data['form_materiales_perdida'] = Detalle_perdidas_materialesForm()
    data['action'] = 'finalizar'
    for d in Detalle_produccion.objects.filter(produccion_id=produccion.id):
        pro = d.producto.toJSON()
        pro['cantidad'] = d.cantidad
        pro['cantidad_estimada'] = d.cantidad
        pro['perdida'] = 0
        productos.append(pro)
    data['productos'] = productos
    return render(request, 'front-end/produccion/produccion_form.html', data)


