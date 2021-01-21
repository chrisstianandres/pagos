from django import forms
from django.forms import TextInput

from apps.tipo_material.models import Tipo_material


class Tipo_materialForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del tipo de material', 'class': 'form-control',
                       'id': 'id_nombre_tipo_material'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Tipo_material
        fields = ['nombre']
        labels = {'nombre': 'Nombre'}
        widgets = {'nombre': forms.TextInput()}
