from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos nombres', 'class': 'form-control form-rounded'})
            self.fields['num_doc'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de docuemnto', 'class': 'form-control form-rounded'})
            self.fields['correo'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control form-rounded'})
            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el numero de telefono', 'class': 'form-control form-rounded'})
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una direccion', 'class': 'form-control form-rounded'})
            # self.fields['sexo'].widget.attrs['class'] = 'selectpicker'
            # self.fields["fecha_nacimiento"].widget = SelectDateWidget(years=years,
            #                                                         attrs={'class': 'selectpicker'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = Proveedor
        fields = ['nombre',
                  'tipo',
                  'num_doc',
                  'correo',
                  'telefono',
                  'direccion'
                  ]
        labels = {
            'nombres': 'Nombre',
            'tipo': 'Tipo de Documento',
            'num_doc': 'N° de Documento',
            'correo': 'Correo',
            'telefono': 'Telefono',
            'direccion': 'Direccion'

        }
        widgets = {
            'nombre': forms.TextInput(),
            'tipo': forms.Select(attrs={'class': 'selectpicker', 'data-width': 'fit'}),
            'num_doc': forms.TextInput(),
            'correo': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'direccion': forms.Textarea()
        }
