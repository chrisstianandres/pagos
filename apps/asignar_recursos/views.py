import json

from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse, HttpResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.asignar_recursos.forms import Asig_recursoForm, Detalle_Asig_recursoForm, Detalle_Asig_maquinaForm, \
    NovedadesForm
from apps.asignar_recursos.models import Asig_recurso, Detalle_asig_recurso, Detalle_asig_maquina, Detalle_produccion, \
    Novedades, Detalle_perdidas_materiales
from apps.backEnd import nombre_empresa
from apps.maquina.models import Maquina
from apps.material.models import Material
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.models import Producto
from apps.producto_base.models import Producto_base

opc_icono = 'fas fa-toolbox'
opc_entidad = 'Confeccion de Prendas'
crud = '/asignar/crear'
empresa = nombre_empresa()


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
                    for m in Detalle_asig_maquina.objects.filter(asig_recurso_id=id):
                        for x in Maquina.objects.filter(id=m.maquina.pk):
                            x.estado = 0
                            x.save()
                    for d in asignar.detalle_produccion_set.all():
                        prd = Producto.objects.get(id=d.producto.id)
                        prd.stock += d.cantidad
                        prd.save()
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
        data['titulo'] = 'Listado de Confecciones'
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
                        c.lote = datos['lote']
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

# query = Distribucion.objects.get(id=id, lote__estado=0)
#                 lote_data = [query.toJSON()]
#                 for p in query.peso_set.all():
#                     peso_data.append(p.toJSON())
# class lista(SuperUserRequiredMixin, ListView):
#     model = Asig_insumo
#     template_name = 'front-end/asig_insumo/asig_insumo_list.html'
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['icono'] = opc_icono
#         data['entidad'] = opc_entidad
#         data['boton'] = 'Nueva Asignacion de Insumos'
#         data['titulo'] = 'Listado de Asignacion de Insumos'
#         data['nuevo'] = '/asig_insumo/nuevo'
#         return data

#
# def nuevo(request):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../compra/get_insumo',
#         'boton': 'Guardar Asignacion', 'action': 'add', 'titulo': 'Nuevo Registro de una Asognacion',
#         'key': ''
#     }
#     if request.method == 'GET':
#         data['form'] = Asig_InsumoForm()
#         data['form2'] = Detalle_Asig_InsumoForm()
#         data['detalle'] = []
#     return render(request, 'front-end/asig_insumo/asig_insumo_form.html', data)
#
#
# @csrf_exempt
# def crear(request):
#     data = {}
#     if request.method == 'POST':
#         datos = json.loads(request.POST['asignar'])
#         if datos:
#             with transaction.atomic():
#                 c = Asig_insumo()
#                 c.fecha_asig = datos['fecha_asig']
#                 c.periodo_id = datos['periodo']
#                 c.cantero_id = datos['cantero']
#                 c.save()
#                 for i in datos['insumos']:
#                     dv = Detalle_asig_insumo()
#                     dv.asig_insumo_id = c.id
#                     dv.insumo_id = i['id']
#                     dv.cantidad = int(i['cantidad'])
#                     print(i['cantidad'])
#                     dv.save()
#                     x = Insumo.objects.get(pk=i['id'])
#                     x.stock = x.stock - int(i['cantidad'])
#                     x.save()
#                     data['resp'] = True
#         else:
#             data['resp'] = False
#             data['error'] = "Datos Incompletos"
#     return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# def editar(request, id):
#     data = {
#         'icono': opc_icono, 'entidad': opc_entidad, 'crud': '../../asig_insumo/get_insumo',
#         'boton': 'Editar Asignacion de Insumos', 'action': 'edit', 'titulo': 'Editar Registro de una Asignacion',
#         'key': id
#     }
#     asig_insumo = Asig_insumo.objects.get(id=id)
#     if request.method == 'GET':
#         data['form'] = Asig_InsumoForm(instance=asig_insumo)
#         data['form2'] = Detalle_asig_insumo()
#         data['detalle'] = json.dumps(get_detalle_productos(id))
#     return render(request, 'front-end/asig_insumo/asig_insumo_form.html', data)
#
#
# @csrf_exempt
# def editar_save(request):
#     data = {}
#     datos = json.loads(request.POST['asignar'])
#     if request.POST['action'] == 'edit':
#
#         with transaction.atomic():
#             # c = Compra.objects.get(pk=self.get_object().id)
#             c = Asig_insumo.objects.get(pk=request.POST['key'])
#             c.fecha_asig = datos['fecha_asig']
#             c.cantero_id = datos['cantero']
#             c.periodo_id = datos['periodo']
#             c.save()
#             c.detalle_asig_insumo_set.all().delete()
#             for i in datos['insumos']:
#                 dv = Detalle_asig_insumo()
#                 dv.asig_insumo_id = c.id
#                 dv.insumo_id = i['id']
#                 dv.cantidad = int(i['cantidad'])
#                 dv.save()
#                 x = Insumo.objects.get(pk=i['id'])
#                 x.stock = x.stock - int(i['cantidad'])
#                 x.save()
#                 data['resp'] = True
#     else:
#         data['resp'] = False
#         data['error'] = "Datos Incompletos"
#     return HttpResponse(json.dumps(data), content_type="application/json")
#
#
# def get_detalle_productos(id):
#     data = []
#     try:
#         for i in Detalle_asig_insumo.objects.filter(compra_id=id):
#             item = i.insumo.toJSON()
#             item['cantidad'] = i.cantidad
#             data.append(item)
#     except:
#         pass
#     return data
#
#
# @csrf_exempt
# def get_insumo(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             insumo = Insumo.objects.filter(pk=id)
#             data = []
#             for i in insumo:
#                 item = i.toJSON()
#                 item['cantidad'] = 1
#                 data.append(item)
#         else:
#             data['error'] = 'No ha selecionado ningun Insumo'
#     except Exception as e:
#         data['error'] = 'Ha ocurrido un error'
#     return JsonResponse(data, safe=False)
#
#
# @csrf_exempt
# def get_detalle(request):
#     data = {}
#     try:
#         id = request.POST['id']
#         if id:
#             data = []
#             for p in Detalle_asig_insumo.objects.filter(asig_insumo__cantero_id=id):
#                 data.append(p.toJSON())
#         else:
#             data['error'] = 'Ha ocurrido un error'
#     except Exception as e:
#         data['error'] = str(e)
#     return JsonResponse(data, safe=False)
#
#
# def report(request):
#     data = { 'icono': opc_icono, 'entidad': opc_entidad, 'titulo': 'Reporte de Asignacion de Isumos', 'key': ''}
#     return render(request, 'front-end/asig_insumo/asig_insumo_report.html', data)
#
#
# @csrf_exempt
# def data(request):
#     data = []
#     start_date = request.POST.get('start_date', '')
#     end_date = request.POST.get('end_date', '')
#     try:
#         if start_date == '' and end_date == '':
#             asig_insumo = Detalle_asig_insumo.objects.all()
#             for c in asig_insumo:
#                 data.append([
#                     c.id,
#                     c.asig_insumo.fecha_asig.strftime('%d-%m-%Y'),
#                     c.asig_insumo.periodo.nombre,
#                     c.asig_insumo.cantero.nombre,
#                     c.insumo.nombre,
#                     c.insumo.categoria.nombre,
#                     c.insumo.presentacion.nombre,
#                     c.cantidad
#                 ])
#         else:
#             asig_insumo = Detalle_asig_insumo.objects.filter(asig_insumo__fecha_asig__range=[start_date, end_date])
#             for c in asig_insumo:
#                 data.append([
#                     c.id,
#                     c.asig_insumo.fecha_asig.strftime('%d-%m-%Y'),
#                     c.asig_insumo.periodo.nombre,
#                     c.asig_insumo.cantero.nombre,
#                     c.insumo.nombre,
#                     c.insumo.categoria.nombre,
#                     c.insumo.presentacion.nombre,
#                     c.cantidad
#                 ])
#     except:
#         pass
#     return JsonResponse(data, safe=False)
