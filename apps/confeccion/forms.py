from django import forms
from datetime import *
from .models import Reparacion, Detalle_reparacion
from tempus_dominus.widgets import DatePicker

from ..cliente.models import Cliente
# from ..inventario.models import Inventario
from ..producto.models import Producto


class ReparacionForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_ingreso'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['fecha_entrega'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['cliente'].widget.attrs = {
                'class': 'custom-select select2'
            }
            self.fields["cliente"].queryset = Cliente.objects.none()
            self.fields['subtotal'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }
            self.fields['iva'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }
            self.fields['total'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }

        # habilitar, desabilitar, y mas

    class Meta:
        model = Reparacion
        fields = [
            'fecha_ingreso',
            'fecha_entrega',
            'cliente',
            'subtotal',
            'iva',
            'total'
        ]
        labels = {
            'fecha_ingreso': 'Fecha de Recepcion',
            'fecha_entrega': 'Fecha de Entrega',
            'cliente': 'Cliente',
            'subtotal': 'Subtotal',
            'iva': 'I.V.A.',
            'total': 'TOTAL'
        }
        widgets = {
            'fecha_ingreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'fecha_entrega': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'subtotal': forms.TextInput(),
            'iva': forms.TextInput(),
            'total': forms.TextInput(),
        }


class Detalle_reparacionform(forms.ModelForm):
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
        model = Detalle_reparacion
        fields = [
            'producto'
        ]