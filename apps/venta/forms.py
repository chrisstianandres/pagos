from django import forms

from .models import Detalle_venta
from ..asignar_recursos.models import Detalle_produccion


class Detalle_VentaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['inventario'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
            self.fields["inventario"].queryset = Detalle_produccion.objects.none()
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_venta
        fields = [
            'inventario',
        ]
