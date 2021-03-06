from django import forms
from datetime import *
from .models import Produccion, Detalle_perdidas_materiales, Detalle_perdidas_productos
from apps.inventario_productos.models import Inventario_producto
from tempus_dominus.widgets import DatePicker

from apps.producto.models import Producto
from apps.maquina.models import Maquina
from ..asignar_recursos.models import Asig_recurso
from ..material.models import Material

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


class ProduccionForm(forms.ModelForm):
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
            self.fields['novedades'].widget.attrs = {
                'class': 'form-control'
            }
        #     self.fields["cliente"].queryset = Cliente.objects.none()
        # habilitar, desabilitar, y mas

    class Meta:
        model = Produccion
        fields = [
            'fecha_ingreso',
            'novedades',

        ]
        labels = {
            'fecha_ingreso': 'Fecha fin de Produccion',
            'novedades': 'Novedades',
        }
        widgets = {
            'fecha_ingreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'novedades': forms.Textarea()
        }


class Detalle_perdidas_materialesForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['material'].widget.attrs = {
                'class': 'form-control select2',
                'style': 'width: 100%'
            }
            self.fields["material"].queryset = Material.objects.none()
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_perdidas_materiales
        fields = [
            'material'
        ]

