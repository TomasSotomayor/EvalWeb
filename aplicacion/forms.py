# forms.py

from django import forms
from .models import TipoUsuario, Usuario

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['nombre']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password', 'tipo_usuario']

