from django import forms
from datetime import *

from django.db import transaction
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Cliente
from ..user.models import User


class ClienteForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['first_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos nombres', 'class': 'form-control form-rounded'})
            self.fields['last_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos Apellidos', 'class': 'form-control form-rounded'})
            self.fields['cedula'].widget = TextInput(
                attrs={'placeholder': 'Ingrese un numero de cedula', 'class': 'form-control form-rounded'})
            self.fields['email'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control form-rounded'})
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una direccion (Maximo 50 caracteres)', 'class': 'form-control form-rounded'})
            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de telefono', 'class': 'form-control form-rounded'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'cedula',
                  'email',
                  'sexo',
                  'telefono',
                  'celular',
                  'direccion'
                  ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'cedula': 'N° de cedula',
            'email': 'Correo',
            'sexo': 'Genero',
            'Telefono': 'Telefono',
            'celular': 'Celular',
            'Direccion': 'direccion'

        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'cedula': forms.TextInput(),
            'sexo': forms.Select(attrs={'class': 'selectpicker', 'data-width': 'fit'}),
            'email': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'celular': forms.TextInput(),
            'direccion': forms.TextInput()
        }

    @transaction.atomic()
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['cedula']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                nombres = self.cleaned_data['first_name']
                apellidos = self.cleaned_data['last_name']
                cedula = self.cleaned_data['cedula']
                sexo = self.cleaned_data['sexo']
                telefono = self.cleaned_data['telefono']
                correo = self.cleaned_data['email']
                cliente = Cliente(
                    nombres=nombres,
                    apellidos=apellidos,
                    cedula=cedula,
                    correo=correo,
                    sexo=sexo,
                    telefono=telefono,
                    direccion='Sin direccion'
                )
                cliente.save()
                u.save()
                print(u.id)
                grupo = Group.objects.get(name__icontains='cliente')
                usersave = User.objects.get(id=u.id)
                usersave.groups.add(grupo)
                usersave.tipo = 0
                usersave.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
