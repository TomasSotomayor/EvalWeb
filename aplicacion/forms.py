# forms.py

from django import forms
from .models import TipoUsuario,TipoProducto, Usuario

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['nombre']
