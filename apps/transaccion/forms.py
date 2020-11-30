from django import forms
from datetime import *
from .models import Transaccion
from tempus_dominus.widgets import DatePicker

from ..cliente.models import Cliente
from ..inventario.models import Inventario
from ..producto.models import Producto


class TransaccionForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_trans'].widget.attrs = {
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
        model = Transaccion
        fields = [
            'fecha_trans',
            'cliente',
            'subtotal',
            'iva',
            'total'
        ]
        labels = {
            'fecha_trans': 'Fecha',
            'cliente': 'Cliente',
            'subtotal': 'Subtotal',
            'iva': 'I.V.A.',
            'total': 'TOTAL'
        }
        widgets = {
            'fecha_trans': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'subtotal': forms.TextInput(),
            'iva': forms.TextInput(),
            'total': forms.TextInput(),
        }
