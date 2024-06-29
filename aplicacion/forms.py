# forms.py

from django import forms
from .models import TipoUsuario

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['nombre']
