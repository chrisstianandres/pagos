from django import forms
from datetime import *
from .models import Asig_insumo, Detalle_asig_insumo
from tempus_dominus.widgets import DatePicker

from apps.producto.models import Producto
from apps.maquina.models import Maquina
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
            self.fields['periodo'].widget.attrs = {
                'class': 'form-control',
                # 'value': Periodo.objects.get(estado=0),
                'disabled': True,
            }
            self.initial['periodo'] = Periodo.objects.get(estado=1)
            self.fields['cantero'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Asig_insumo
        fields = [
            'fecha_asig',
            'periodo',
            'cantero'
        ]
        labels = {
            'fecha_asig': 'Fecha de Asignacion',
            'periodo': 'Periodo',
            'cantero': 'Cantero / Area (m2)'.translate(SUP)
        }
        widgets = {
            'fecha_asig': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            # 'periodo': forms.TextInput()
        }


class Detalle_Asig_InsumoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['insumo'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
            self.fields["insumo"].queryset = Insumo.objects.filter(stock__gte=1)
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_asig_insumo
        fields = [
            'insumo'
        ]
