from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import ActividadForm, DocumentosForm, CronogramaForm, ProgramaForm, CompetenciaForm, RapsForm
from commons.models import T_acti_apre, T_apre, T_acti_ficha, T_ficha, T_crono, T_progra, T_fase_ficha ,T_instru, T_acti_docu, T_perfil, T_compe, T_raps
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def listar_fichas(request):
    perfil = getattr(request.user, 't_perfil', None)
    if perfil is None or perfil.rol != 'instructor':
        return render(request, 'fichas.html', {'mensaje': 'No tienes permisos para acceder a esta página.'})
    
    instructor = T_instru.objects.filter(perfil=perfil).first()

    if not instructor:
        return render(request, 'fichas.html', {'mensaje': 'No se encontraron fichas asociadas a este instructor.'})

    fichas = T_ficha.objects.filter(instru=instructor)
    
    print(fichas)
    return render(request, 'fichas.html', {'fichas': fichas})

@login_required
def panel_ficha(request, ficha_id):
    ficha = get_object_or_404(T_ficha, id=ficha_id)
    actividades = T_acti_ficha.objects.filter(ficha=ficha)
    fase = get_object_or_404(T_fase_ficha, id=ficha_id)
    return render(request, 'panel_instructor.html', {
        'ficha': ficha,
        'actividades': actividades,
        'fase': fase
    })

@login_required
def crear_actividad(request, ficha_id):

    ficha = get_object_or_404(T_ficha, id=ficha_id)
    if request.method == 'GET':

        actividad_form = ActividadForm()
        documento_form = DocumentosForm()
        cronograma_form = CronogramaForm()

        return render(request, 'actividad_crear.html', {
            'ficha': ficha,
            'actividad_form': actividad_form,
            'documento_form': documento_form,
            'cronograma_form': cronograma_form
        })
    else:
        try:
            actividad_form = ActividadForm(request.POST)
            documento_form = DocumentosForm(request.POST, request.FILES)
            cronograma_form = CronogramaForm(request.POST)
            if all([
                actividad_form.is_valid(),
                documento_form.is_valid(),
                cronograma_form.is_valid()
            ]):
                # Obtener el instructor logueado
                try:    
                    perfil = getattr(request.user, 't_perfil', None)
                    instructor = T_instru.objects.get(perfil=perfil)

                except (T_perfil.DoesNotExist, T_instru.DoesNotExist):
                        return render(request, 'actividad_crear.html', {
                            'actividad_form': actividad_form,
                            'documento_form': documento_form,
                            'cronograma_form': cronograma_form,
                            'error': 'No se encontró un instructor asociado al usuario logueado.',
                    })
                
                #Creacion de la actividad
                fase = get_object_or_404(T_fase_ficha, id=ficha_id)

                new_actividad = actividad_form.save(commit=False)
                new_actividad.fase = fase.fase
                new_actividad.save()

                #creacion del documento
                archivo = documento_form.cleaned_data['archi']
                nom = archivo.name
                tipo = archivo.name.split('.')[-1]
                tama = str(archivo.size // 1024) + " KB"

                #Asignacion de atributos al documento
                new_documento = documento_form.save(commit=False)
                new_documento.nom = nom
                new_documento.tipo = tipo
                new_documento.tama = tama
                new_documento.priva = 'No'
                new_documento.esta = 'Activo'
                new_documento.save()

                # Asignar la actividad a el documento
                T_acti_docu.objects.create(
                    docu= new_documento,
                    acti = new_actividad
                )

                # Creacion del cronograma
                new_cronograma = cronograma_form.save()

               # Crear la actividad en T_acti_ficha
                new_acti_ficha = T_acti_ficha.objects.create(
                    ficha=ficha,
                    acti=new_actividad,
                    crono=new_cronograma,    # Si el formulario incluye cronograma
                    esta='Activo'
                )

                # Obtener la lista de aprendices asociados a la ficha
                aprendices = T_apre.objects.filter(ficha=ficha)

                # Crear registros en T_acti_apre
                for aprendiz in aprendices:
                    T_acti_apre.objects.create(
                        apre=aprendiz,
                        acti=new_acti_ficha,
                        apro='Pendiente',  # Estado inicial
                        fecha=now()  # Fecha de asignación
                    )

            return redirect('panel_ficha', ficha_id=ficha.id)

        except ValueError as e:
            return render(request, 'actividad_crear.html', {
            'actividad_form': actividad_form,
            'documento_form': documento_form,
            'cronograma_form': cronograma_form,
            'error': f'Ocurrió un error: {str(e)}'
        })
    #se debe crear la actividad aprendiz aca
    # se debe crear 

@login_required
def panel_aprendiz(request):
    return render(request, 'panel_aprendiz.html')

@login_required
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

# Vistas programa

def listar_programas(request):
    programas = T_progra.objects.all()
    return render(request, 'programas.html', {'programas': programas})

def crear_programa(request):
    if request.method == 'POST':
        programa_form = ProgramaForm(request.POST)
        if programa_form.is_valid():
            programa_form.save()
            return redirect('programas')
    else:
        programa_form = ProgramaForm()
    return render(request, 'crear_programa.html', {'programa_form': programa_form})

# Vistas competencia

def listar_competencias(request):
    competencias = T_compe.objects.all()
    return render(request, 'competencias.html', {'competencias': competencias})

def crear_competencias(request):
    if request.method == 'POST':
        competencia_form = CompetenciaForm(request.POST)
        if competencia_form.is_valid():
            competencia_form.save()
            return redirect('competencias')
    else:
        competencia_form = CompetenciaForm()
    return render(request, 'crear_competencia.html', {'competencia_form': competencia_form})

#Vistas Raps
def listar_raps(request):
    raps = T_raps.objects.all()
    return render(request, 'raps.html', {'raps': raps})

def crear_raps(request):
    if request.method == 'POST':
        raps_form = RapsForm(request.POST)
        if raps_form.is_valid():
            raps_form.save()
            return redirect('raps')
    else:
        raps_form = RapsForm()
    return  render(request, 'crear_raps.html', {'raps_form': raps_form})
