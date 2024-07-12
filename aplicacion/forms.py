# forms.py

from django import forms
from .models import TipoUsuario,TipoProducto, Usuario,Promocion

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['nombre']

class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['nombre']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre','email','password','tipo_usuario']

class PromocionForm(forms.ModelForm):
    class Meta:
        model = Promocion
        fields = ['descripcion','descuento']

        