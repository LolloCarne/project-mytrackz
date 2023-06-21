from django.shortcuts import render

# Create your views here.

def prova(request):
    return render(request,'aggiornaStato/prova.html')