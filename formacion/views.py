from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def panel_instructor(request):

    return render(request, 'panel_instructor.html')

def panel_aprendiz(request):
    return render(request, 'panel_aprendiz.html')

def tree_detalle(request):
    data = [
    {
        "title": "PLAN DE TRABAJO CONCERTADO CON SUS DESCRIPTORES",
        "id": "1",
        "children": [
            {"title": "Fase Analisis", "id": "1"},
            {"title": "Fase Planeacion", "id": "2"},
            {"title": "Fase Ejecucion", "id": "3"},
            {"title": "Fase Evaluacion", "id": "4"}
        ]
    },
    {
        "title": "GFPI F 135 GUIA DE APRENDIZAJE",
        "id": "2",
        "children": [
            {
                "title": "Fase Analisis",
                "id": "1",
                "children": [
                    {"title": "Guia de la fase", "id": "1"},
                    {"title": "Instrumentos de evaluacion", "id": "2"}
                ]
            },
            {"title": "Fase Planeacion", "id": "2"},
            {"title": "Fase Ejecucion", "id": "3"},
            {"title": "Fase Evaluacion", "id": "4"}
        ]
    }
    ]
    return JsonResponse(data, safe=False)