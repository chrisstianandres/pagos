import json

from django.db.models import Q, Sum, Count
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.asignar_recursos.models import Detalle_asig_recurso, Asig_recurso
from apps.backEnd import nombre_empresa
from apps.categoria.forms import CategoriaForm
from apps.color.forms import ColorForm
from apps.compra.models import Detalle_compra

from apps.material.forms import MaterialForm, Producto_baseForm
from apps.material.models import Material
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto_base.models import Producto_base
from apps.tipo_material.forms import Tipo_materialForm

opc_icono = 'fas fa-hat-cowboy-side'
opc_entidad = 'Material'
crud = '/material/nuevo'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Material
    template_name = 'front-end/material/material_list.html'
    permission_required = 'material.view_material'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Material.objects.all():
                    data.append(c.toJSON())
            elif action == 'list_compra':
                data = []
                ids = json.loads(request.POST['ids'])
                query = Material.objects.all()
                for c in query.exclude(producto_base_id__in=ids):
                    data.append(c.toJSON())
            elif action == 'search':
                data = []
                term = request.POST['term']
                ids = json.loads(request.POST['ids'])
                query = Material.objects.filter(producto_base__nombre__icontains=term)
                for a in query.exclude(producto_base_id__in=ids)[0:10]:
                    result = {'id': int(a.id), 'text': str(a.producto_base.nombre)}
                    data.append(result)
            elif action == 'search_perd':
                data = []
                term = request.POST['term']
                lote = request.POST['asig']
                asig = Asig_recurso.objects.get(lote=lote)
                query = Detalle_asig_recurso.\
                            objects.filter(inventario_material__material__producto_base__nombre__icontains=term, asig_recurso_id=int(asig.id)).\
                            values('inventario_material__material__producto_base_id',
                                   'asig_recurso_id',
                                   'inventario_material__material_id'
                                   ).annotate(total=Count('id')).\
                            order_by('-total')[0:10]
                for i in query:
                    px = Material.objects.get(id=int(i['inventario_material__material_id']))
                    result = {'id': int(px.id), 'text': str(px.producto_base.nombre)}
                    data.append(result)
            elif action == 'get':
                print(request.POST)
                # id = request.POST['id']
                # asig = request.POST['asig[id]']
                #
                # material = Detalle_asig_recurso.objects.filter(asig_recurso_id=int(asig)).values('inventario_material__material__producto_base')
                data = []
                # for i in material:
                #     item = i.toJSON()
                #     item['cantidad'] = 1
                #     item['subtotal'] = 0.00
                #     item['iva_emp'] = 12
                #     cal = format(float((i.p_compra*100)/112), '.2f')
                #     item['p_compra'] = cal
                #     data.append(item)
            elif action == 'search_asig':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                que = self.model.objects.filter(Q(producto_base__nombre__icontains=term) |
                                                Q(color__nombre__icontains=term), stock_actual__gte=5)
                for a in que.exclude(id__in=ids)[0:10]:
                    result = {'id': a.id, 'text': str(str(a.producto_base.nombre) + ' / ' + str(a.color))}
                    data.append(result)
            elif action == 'get_asig':
                id = request.POST['id']
                material = Material.objects.get(pk=id)
                data = []
                item = material.toJSON()
                item['cantidad'] = 5
                item['iva_emp'] = empresa.iva
                data.append(item)
            elif action == 'search_asig_table':
                data = []
                ids = json.loads(request.POST['ids'])
                que = self.model.objects.filter(stock_actual__gte=5)
                for a in que.exclude(id__in=ids):
                    result = a.toJSON()
                    result['cantidad'] = 5
                    data.append(result)
            elif action == 'get_perd':
                id = request.POST['id']
                max = Detalle_asig_recurso.objects.filter(inventario_material__material_id=id).count()
                data = []
                m = Material.objects.get(id=id)
                item = m.producto_base.toJSON()
                item['id'] = m.id
                item['calidad'] = m.get_calidad_display()
                item['tipo'] = m.tipo_material.nombre
                item['medida'] = m.medida
                item['ud_medida'] = m.ud_medida
                item['cantidad'] = 1
                item['max'] = int(max)
                data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Material'
        data['titulo'] = 'Listado de Materiales'
        data['nuevo'] = '/material/nuevo'
        data['empresa'] = empresa
        return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Material
    template_name = 'front-end/material/material_report.html'
    permission_required = 'material.view_material'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                data = []
                for c in self.model.objects.all():
                    item = c.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Reporte de Stock de Materiales'
        data['titulo'] = 'Reporte de Materiales'
        data['empresa'] = empresa
        return data


class Createview(ValidatePermissionRequiredMixin, CreateView):
    model = Producto_base
    second_model = Material
    form_class = Producto_baseForm
    second_form_class = MaterialForm
    success_url = 'material:lista'
    template_name = 'front-end/material/material_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                self.object = self.get_object
                f = self.form_class(request.POST)
                f2 = self.second_form_class(request.POST)
                data = self.save_data(f, f2)
                return HttpResponseRedirect(reverse_lazy('material:lista'))
            elif action == 'delete':
                pk = request.POST['id']
                f = Material.objects.get(pk=pk)
                f2 = Producto_base.objects.get(id=f.producto_base_id)
                f.delete()
                f2.delete()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f, f2):
        data = {}
        if f.is_valid() and f2.is_valid():
            base = f2.save(commit=False)
            b = f.save()
            base.producto_base = b
            base.save()
            mat = Producto_base.objects.get(pk=b.id)
            mat.tipo = 1
            mat.save()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'form' not in data:
            data['form'] = self.form_class(self.request.GET)
        if 'form2' not in data:
            data['form2'] = self.second_form_class(self.request.GET)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Material'
        data['titulo'] = 'Nuevo Registro de un Material'
        data['nuevo'] = '/material/nuevo'
        data['action'] = 'add'
        data['crud'] = crud
        data['form_cat'] = CategoriaForm
        data['form_tipo'] = Tipo_materialForm
        data['form_color'] = ColorForm
        data['empresa'] = empresa
        return data


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    second_model = Producto_base
    second_form_class = Producto_baseForm
    success_url = reverse_lazy('material:lista')
    template_name = 'front-end/material/material_form.html'
    permission_required = 'material.change_material'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            material = self.model.objects.get(id=pk)
            producto_base = self.second_model.objects.get(id=material.producto_base_id)
            if action == 'edit':
                f = self.second_form_class(request.POST, instance=producto_base)
                f2 = self.form_class(request.POST, instance=material)
                data = self.save_data(f, f2)
                return HttpResponseRedirect(reverse_lazy('material:lista'))
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f, f2):
        data = {}
        if f.is_valid() and f2.is_valid():
            f.save()
            f2.save()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super(Updateview, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        material = self.model.objects.get(id=pk)
        producto_base = self.second_model.objects.get(id=material.producto_base_id)
        data['form'] = self.second_form_class(instance=producto_base)
        data['form2'] = self.form_class(instance=material)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Material'
        data['action'] = 'edit'
        data['crud'] = '/material/editar/' + str(self.kwargs['pk'])
        data['form_cat'] = CategoriaForm
        data['empresa'] = empresa
        return data

