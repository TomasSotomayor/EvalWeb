# aplicacion/views.py

from django.shortcuts import render

def arbustos(request):
    return render(request, 'arbustos.html/')

def contacto(request):
    return render(request, 'contacto.html/')

def flores(request):
    return render(request, 'flores.html/')

def index(request):
    return render(request, 'index.html/')

def maceteros(request):
    return render(request, 'maceteros.html/')

def registro(request):
    return render(request, 'registro.html/')

def tierrahoja(request):
    return render(request, 'tierrahoja.html/')
