# forms.py

from django import forms
from .models import TipoUsuario,TipoProducto

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['nombre']


class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['nombre']
