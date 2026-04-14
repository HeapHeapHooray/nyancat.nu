from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def converter(request):
    return render(request, 'core/converter.html')

