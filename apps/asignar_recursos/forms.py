from django import forms
from datetime import *
from .models import Asig_recurso, Detalle_asig_recurso, Detalle_asig_maquina, Novedades
from tempus_dominus.widgets import DatePicker

from apps.producto.models import Producto
from apps.maquina.models import Maquina
from ..material.models import Material

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


class Asig_recursoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_asig'].widget.attrs = {
                'readonly': True,
                'class': 'form-control'
            }
            self.fields['lote'].widget.attrs = {
                'class': 'form-control'
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Asig_recurso
        fields = [
            'fecha_asig',
            'lote',

        ]
        labels = {
            'fecha_asig': 'Duracion de Produccion',
            'lote': 'Lote',
        }
        widgets = {
            'fecha_asig': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
        }


class Detalle_Asig_recursoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['inventario_material'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
            self.fields["inventario_material"].queryset = Material.objects.none()
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_asig_recurso
        fields = [
            'inventario_material'
        ]


class Detalle_Asig_maquinaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['maquina'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true",
                'style': 'width: 90%'
            }
            self.fields["maquina"].queryset = Maquina.objects.none()
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_asig_maquina
        fields = [
            'maquina'
        ]


class NovedadesForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['novedad'].widget.attrs = {
                'class': 'form-control',
                'placeholder': 'Ingrese una novedad con maximo 200 caracteres'
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Novedades
        fields = [
            'fecha',
            'novedad'
        ]
        labels = {
            'novedad': 'Novedad',
            'fecha': 'Fecha',
        }
        widgets = {
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'novedad': forms.Textarea()
        }