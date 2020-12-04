from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from apps.backEnd import nombre_empresa
from apps.delvoluciones_venta.models import Devolucion

opc_icono = 'fas fa-exchange-alt'
opc_entidad = 'Devoluciones de ventas'
crud = '/devoluciones/crear'
empresa = nombre_empresa()


class lista(ListView):
    model = Devolucion
    template_name = 'front-end/devoluciones/devolucion_report_total.html'

    def get_queryset(self):
        return Devolucion.objects.none()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte  de Devoluciones'
        data['empresa'] = empresa
        return data


@csrf_exempt
def data(request):
    data = []
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    venta = ''
    estado = ''
    try:
        if start_date == '' and end_date == '':
            devolucion = Devolucion.objects.all()
        else:
            devolucion = Devolucion.objects.filter(fecha__range=[start_date, end_date])
        for c in devolucion:
            data.append([
                c.id,
                c.fecha,
                c.venta.fecha_venta,
                c.venta.cliente.nombres + ' ' + c.venta.cliente.apellidos,
                c.venta.empleado.get_full_name(),
                c.venta.id,
                format(c.venta.total, '.2f'),
                c.id
            ])

    except:
        pass
    return JsonResponse(data, safe=False)