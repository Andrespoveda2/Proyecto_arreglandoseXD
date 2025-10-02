from django.shortcuts import render
from django.http import HttpResponse

# views.py en la app home

def index(request):
    return render(request, 'index.html')

def acerca_de(request):
    return render(request, 'acerca_de.html')
