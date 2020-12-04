from django import forms
from datetime import *
from .models import Confeccion, Detalle_confeccion
from tempus_dominus.widgets import DatePicker

from ..cliente.models import Cliente
# from ..inventario.models import Inventario
from ..producto.models import Producto


class ConfeccionForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_entrega'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Confeccion
        fields = [
            'fecha_entrega'
        ]
        labels = {
            'fecha_entrega': 'Fecha de Entrega'
        }
        widgets = {
            'fecha_entrega': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            )
        }


class Detalle_confeccionform(forms.ModelForm):
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
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_confeccion
        fields = [
            'producto'
        ]