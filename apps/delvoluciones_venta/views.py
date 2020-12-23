from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from apps.backEnd import nombre_empresa
from apps.delvoluciones_venta.models import Devolucion
from apps.mixins import ValidatePermissionRequiredMixin

opc_icono = 'fas fa-exchange-alt'
opc_entidad = 'Devoluciones de ventas'
crud = '/devoluciones/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Devolucion
    template_name = 'front-end/devoluciones/devolucion_report_total.html'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Devolucion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:

            action = request.POST['action']
            if action == 'report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                venta = ''
                estado = ''
                if start_date == '' and end_date == '':
                    devolucion = Devolucion.objects.all()
                else:
                    devolucion = Devolucion.objects.filter(fecha__range=[start_date, end_date])
                for c in devolucion:
                    data.append([
                        c.id,
                        c.fecha,
                        c.venta.transaccion.fecha_trans,
                        c.venta.transaccion.cliente.nombres + ' ' + c.venta.transaccion.cliente.apellidos,
                        c.venta.transaccion.user.get_full_name(),
                        c.venta.id,
                        format(c.venta.transaccion.total, '.2f'),
                        c.id
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte  de Devoluciones'
        data['empresa'] = empresa
        return data