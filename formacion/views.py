from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def panel_instructor(request):

    return render(request, 'panel_instructor.html')

def panel_aprendiz(request):
    return render(request, 'panel_aprendiz.html')

def tree_detalle(request):
    data = [
        {"title": "Raíz", "id": "1", "children": [
            {"title": "Hijo 1", "id": "2"},
            {"title": "Hijo 2", "id": "3"}
        ]}
    ]
    return JsonResponse(data, safe=False)