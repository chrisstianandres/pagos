from django import forms
from django.forms import TextInput

from apps.material.models import Material
from apps.producto_base.models import Producto_base


class MaterialForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['p_compra'].widget.attrs = {'class': 'form-control form-control-sm input-sm',
                                                    'value': 1}
            self.fields['calidad'].widget.attrs = {
                'class': 'form-control select2'}
            self.fields['tipo_material'].widget.attrs = {
                'class': 'form-control select2'}
            self.fields['color'].widget.attrs = {
                'class': 'form-control select2'}

    class Meta:
        model = Material
        fields = ['p_compra', 'color', 'calidad', 'tipo_material', 'unidad_medida']
        labels = {'p_compra': 'P. Compra Unitario', 'color': 'Color', 'calidad': 'Calidad',
                  'tipo_material': 'Tipo de Material', 'unidad_medida': 'Medida'}
        widgets = {'p_compra': forms.TextInput()}


class Producto_baseForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del producto', 'class': 'form-control form-rounded'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion del producto', 'class': 'form-control form-rounded'})
            self.fields['categoria'].widget.attrs = {
                'class': 'form-control select2'}

    class Meta:
        model = Producto_base
        fields = ['nombre',
                  'descripcion',
                  'categoria'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Decripcion',
            'categoria': 'Categoria'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'decripcion': forms.Textarea(attrs={'col': '3', 'row': '2'})
        }
