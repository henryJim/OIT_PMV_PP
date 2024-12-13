from django.shortcuts import render

# Create your views here.

def panel_instructor(request):

    return render(request, 'panel_instructor.html')

def panel_aprendiz(request):
    return render(request, 'panel_aprendiz.html')