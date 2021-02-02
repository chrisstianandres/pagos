from django import forms
from datetime import *
from .models import Compra, Detalle_compra


class CompraForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_compra'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['proveedor'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true",
                'style': "width: 80%"
            }
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
        model = Compra
        fields = [
            'fecha_compra',
            'proveedor',
            'subtotal',
            'iva',
            'total'
        ]
        labels = {
            'fecha_compra': 'Fecha de Compra',
            'proveedor': 'Proveedor',
            'subtotal': 'Subtotal',
            'iva': 'I.V.A.',
            'total': 'TOTAL'
        }
        widgets = {
            'fecha_compra': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'iva': forms.TextInput(),
            'total': forms.TextInput(),
        }


class Detalle_CompraForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['material'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_compra
        fields = [
            'material'
        ]
