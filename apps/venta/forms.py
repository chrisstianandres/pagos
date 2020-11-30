from django import forms
from datetime import *
from .models import Venta, Detalle_venta
from tempus_dominus.widgets import DatePicker

from ..cliente.models import Cliente
from ..inventario.models import Inventario
from ..producto.models import Producto


class Detalle_VentaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['producto'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
            self.fields["producto"].queryset = Inventario.objects.none()
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_venta
        fields = [
            'producto',
        ]
