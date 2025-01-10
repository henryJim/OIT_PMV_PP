from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from commons.models import T_ficha, T_prematri_docu, T_apre
from .forms import AsignarAprendicesFichaForm
from .scripts.cargar_tree_apre import crear_datos_prueba_aprendiz
from datetime import datetime
import zipfile
import io
import os


# Create your views here.
@login_required
def fichas_prematricula(request):
    # Filtrar las fichas por estado "pre matrícula"
    fichas = T_ficha.objects.all()  # Asegúrate de que el campo 'estado' exista y tenga este valor.
    
    # Renderizar la plantilla con las fichas filtradas
    return render(request, 'fichas_prematricula.html', {
        'fichas': fichas
    })

@login_required
def asignar_aprendices(request, ficha_id):
    ficha = get_object_or_404(T_ficha, id=ficha_id)  # Obtén la ficha al inicio

    if request.method == 'POST':
        aprendiz_asi_form = AsignarAprendicesFichaForm(request.POST)

        if aprendiz_asi_form.is_valid():  # Valida el formulario
            # Cambia el estado de la ficha
            ficha.esta = 'Validacion matriculas'
            ficha.save()

            documentos_matricula = [
                'Documento de identidad',
                'EPS',
                'Cesion de derechos',
                'Formato inscripcion de matriculas',
                'Formato inscripcion proyecto etapa productiva',
                'Formato compromiso aprendiz',
                'Formato tratamiento de datos del menor'
            ]

            # Asigna los aprendices a la ficha
            aprendices = aprendiz_asi_form.cleaned_data['aprendices']
            for aprendiz in aprendices:
                aprendiz.ficha = ficha
                aprendiz.save()
                # Crea datos de prueba asociados al aprendiz
                crear_datos_prueba_aprendiz(ficha.id, aprendiz.id)
                # Crea los documenos de matricula del aprendiz
                for documento in documentos_matricula:
                    new_documento = T_prematri_docu()
                    new_documento.nom = documento
                    new_documento.apren = aprendiz
                    new_documento.esta = "Pendiente"
                    new_documento.vali = "0"
                    new_documento.save()

            return redirect('pre_matricula')
        else:
            return render(request, 'asignar_aprendices.html', {
                'aprendiz_asi_form': aprendiz_asi_form,
                'error': 'Formulario no válido. Revisa los datos ingresados.'
            })
    else:
        aprendiz_asi_form = AsignarAprendicesFichaForm()

    return render(request, 'asignar_aprendices.html', {
        'aprendiz_asi_form': aprendiz_asi_form
    })



@login_required
def confirmar_documentacion(request, ficha_id):
    ficha = T_ficha.objects.get(id=ficha_id)
    ficha.esta = 'Matriculada'
    ficha.save()
    return redirect('pre_matricula')

@login_required
def ver_docs_prematricula_ficha(request, ficha_id):
    # Obtener la ficha por ID
    ficha = get_object_or_404(T_ficha, id=ficha_id)
    
    # Obtener los aprendices de la ficha
    aprendices = T_apre.objects.filter(ficha=ficha)
    
    # Obtener documentos por aprendiz
    documentos_por_aprendiz = {}
    for aprendiz in aprendices:
        documentos = T_prematri_docu.objects.filter(apren=aprendiz)
        documentos_por_aprendiz[aprendiz] = documentos

    return render(request, 'detalle_docs_prematricula.html', {
        'ficha': ficha,
        'documentos_por_aprendiz': documentos_por_aprendiz,
    })

def descargar_documentos_zip(request, aprendiz_id):
    # Obtén todos los documentos del estudiante
    aprendiz = get_object_or_404(T_apre, id=aprendiz_id)
    documentos = T_prematri_docu.objects.filter(apren=aprendiz)

    # Crea un archivo ZIP en memoria
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for documento in documentos:
            if documento.docu and documento.docu.archi:
                # Obtén el archivo del documento
                archivo = documento.docu.archi
                # Obtén el nombre original del archivo
                nombre_original = os.path.basename(archivo.name)  # Elimina la ruta de la carpeta

                # Escribe el archivo en el ZIP
                with archivo.open('rb') as f:
                    zip_file.writestr(nombre_original, f.read())

    # Prepara la respuesta para enviar el archivo ZIP
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="documentos_{aprendiz.perfil.nom}_{aprendiz.perfil.apelli}.zip"'
    
    return response

def confirmar_documento(request, documento_id, ficha_id):
    ficha = T_ficha.objects.get(id=ficha_id)
    documento = T_prematri_docu.objects.get(id=documento_id)    
    documento.vali = "1"
    documento.usr_apro = request.user
    documento.fecha_apro = datetime.now()
    documento.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))