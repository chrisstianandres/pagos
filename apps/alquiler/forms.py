from django import forms
from datetime import *
from .models import Alquiler, Detalle_alquiler
from ..asignar_recursos.models import Detalle_produccion


class AlquilerForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_salida'].widget.attrs = {
                'class': 'form-control'
            }
            self.fields['fecha_entrega'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Alquiler
        fields = [
            'fecha_salida',
            'fecha_entrega'
        ]
        labels = {
            'fecha_salida': 'Fecha de Salida de las prendas',
            'fecha_entrega': 'Fecha de Entrega'
        }
        widgets = {
            'fecha_salida': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'fecha_entrega': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            )
        }


class Detalle_AlquilerForm(forms.ModelForm):
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
        model = Detalle_alquiler
        fields = [
            'inventario',
        ]
