from django import forms
from django.forms import TextInput

from apps.talla.models import Talla


class TallaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['talla'].widget = TextInput(
                attrs={'class': 'form-control', 'value': 30, 'id': 'id_talla_num'})
            self.fields['eqv_letra'].widget = TextInput(
                attrs={'class': 'form-control'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Talla
        fields = ['talla', 'eqv_letra']
        labels = {'nombre': 'Nombre', 'eqv_letra': 'Equivalencia en letras'}
        widgets = {'nombre': forms.TextInput(), 'eqv_letra': forms.TextInput()}
