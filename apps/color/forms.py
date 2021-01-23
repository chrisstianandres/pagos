from django import forms
from django.forms import TextInput
from .models import Color


class ColorForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del cantero', 'class': 'form-control',
                       'id': 'id_nombre_categoria'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Color
        fields = ['nombre']
        labels = {'nombre': 'Nombre'}
        widgets = {'nombre': forms.TextInput()}
