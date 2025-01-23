from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from commons.models import T_instru,T_cuentas, T_apre,T_docu_labo, T_gestor_depa, T_gestor,T_docu, T_perfil, T_admin, T_lider, T_nove, T_repre_legal, T_munici, T_departa, T_insti_edu, T_centro_forma
from .forms import InstructorForm, PerfilEForm, CustomPasswordChangeForm, DocumentoLaboralForm, GestorForm, PerfilEditForm, GestorDepaForm, CargarAprendicesMasivoForm, UserFormCreate, UserFormEdit, PerfilForm, NovedadForm, AdministradoresForm, AprendizForm, LiderForm, RepresanteLegalForm, DepartamentoForm, MunicipioForm, InstitucionForm, CentroFormacionForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from .serializers import T_insti_edu_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.forms.models import model_to_dict
from io import TextIOWrapper
from django.core.mail import send_mail
from django.db.models import Q  # Para realizar búsquedas dinámicas
from django.conf import settings
from datetime import datetime
from django.db.models import Prefetch
from django.contrib import messages
from django.db import transaction
import csv
import random
import string

def home(request):
    return render(request, 'home.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # Autenticación del usuario
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "El usuario o la contraseña es incorrecto"
            })
        else:
            login(request, user)
            
            # Obtener el perfil del usuario
            try:
                perfil = T_perfil.objects.get(user=user)  # Obtener el perfil asociado al usuario
                
                # Verificar el rol del perfil
                if perfil.rol == 'aprendiz':
                    return redirect('panel_aprendiz')  # Redirigir al panel del aprendiz
                if perfil.rol == 'gestor':
                    return redirect('instituciones_gestor')
            except T_perfil.DoesNotExist:
                pass  # Si no se encuentra el perfil, no hacer nada adicional

            # Si no es aprendiz, redirigir a novedades
            return redirect('novedades')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                email = request.POST['correo']
                if User.objects.filter(email=email).exists():
                    return render(request, 'signup.html', {
                        'error': "El correo ya existe"
                    })
                new_user = User(
                    username=request.POST['username'], 
                    email = request.POST['correo'],
                    first_name = request.POST['nombre'],
                    last_name = request.POST['apellido']
                )
                new_user.set_password(request.POST['password1'])
                new_user.save()
                new_perfil = T_perfil(
                    nom = request.POST['nombre'],
                    apelli= request.POST['apellido'],
                    tipo_dni= request.POST['tipoi'],
                    dni= request.POST['dni'],
                    tele= request.POST['tele'],
                    dire= request.POST['dire'],
                    mail = request.POST['correo'],
                    gene= request.POST['gene'],
                    fecha_naci= request.POST['fechanaci'],
                    rol = 'instructor',
                    user = new_user
                )
                new_perfil.save()
                new_instru = T_instru(
                    esta = 'inscrito',
                    perfil = new_perfil,
                    tipo_vincu = 'web'
                )
                new_instru.save()
                return redirect('signin')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'error': "El usuario ya existe"
                })
    return render(request, 'signup.html', {
        'error': "Las contraseñas no coinciden"
    })

def check_authentication(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({'isAuthenticated': is_authenticated})


@login_required
def perfil(request):
    perfil = getattr(request.user, 't_perfil', None)
    usuario = None

    if perfil.rol == 'instructor':
        usuario = T_instru.objects.get(perfil=perfil)
    elif perfil.rol == 'aprendiz':
        usuario = T_apre.objects.get(perfil=perfil)
    elif perfil.rol == 'lider':
        usuario = T_lider.objects.get(perfil=perfil)
    elif perfil.rol == 'admin':
        usuario = T_admin.objects.get(perfil=perfil)
    elif perfil.rol == 'gestor':
        usuario = T_gestor.objects.get(perfil=perfil)
    elif perfil.rol == 'cuentas':
        usuario = T_cuentas.objects.get(perfil=perfil)

    # Mostrar documentos laborales
    documentos = T_docu_labo.objects.filter(usu=request.user, tipo='laboral')

    # Mostrar documentos laborales
    documentos_aca = T_docu_labo.objects.filter(usu=request.user, tipo='academico')

    # Obtener la hoja de vida del usuario (si existe)
    hoja_vida = T_docu_labo.objects.filter(usu=request.user, tipo='hv').first()

    # Inicializar los formularios por defecto
    form_contraseña = CustomPasswordChangeForm(user=request.user)
    form_documento = DocumentoLaboralForm()
    form_perfil = PerfilForm(instance=perfil)

    # Manejo de las solicitudes POST
    if request.method == 'POST':
        if 'old_password' in request.POST:
            form_contraseña = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form_contraseña.is_valid():
                form_contraseña.save()
                update_session_auth_hash(request, form_contraseña.user)  # Mantener la sesión activa con la nueva contraseña
                logout(request)  # Cerrar sesión para forzar al usuario a iniciar sesión nuevamente

                # Si es una solicitud AJAX, enviar la respuesta adecuada con SweetAlert
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'message': 'Cambio satisfactorio, inicie sesión nuevamente.'})
                else:
                    return redirect('login')  # Si no es AJAX, redirigir al inicio de sesión
            else:
                # Responder con los errores en formato JSON (cuando es AJAX)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'errors': form_contraseña.errors})
                else:
                    messages.error(request, 'Por favor corrige los errores a continuación.')
        elif request.POST.get('form_id') == 'documento_form':
            form_documento = DocumentoLaboralForm(request.POST, request.FILES)
            if form_documento.is_valid():
                # Obtener el archivo cargado
                archivo = request.FILES['documento']

                # Ruta de almacenamiento del archivo
                ruta = f'documentos/instructores/{usuario.perfil.nom}{usuario.perfil.apelli}{usuario.perfil.dni}/laboral/{archivo.name}'
                ruta_guardada = default_storage.save(ruta, archivo)

                # Crear el registro en T_docu
                t_docu = T_docu.objects.create(
                    nom=archivo.name,
                    tipo=archivo.name.split('.')[-1],
                    tama=str(archivo.size // 1024) + " KB",  # Tamaño en KB
                    archi=ruta_guardada,
                    priva='No',  # O cualquier valor adecuado
                    esta='Activo'  # O cualquier estado inicial adecuado
                )

                # Guardar el formulario de DocumentoLaboralForm (sin guardar aún)
                documento = form_documento.save(commit=False)
                documento.usu = request.user  # Asociar el documento al usuario actual
                documento.esta = 'Cargado'  # Estado inicial del documento
                documento.docu = t_docu  # Asignar el documento de T_docu
                documento.tipo = 'laboral'  # Asignar el documento de T_docu
                documento.save()  # Guardar el documento
                messages.success(request, "Documento guardado satisfactoriamente.")

                # Redirigir al perfil después de guardar
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                print(form_documento.errors)  # Imprimir errores para depuración
                messages.error(request, 'Por favor, corrige los errores en el formulario.')

        elif request.POST.get('form_id') == 'documento_aca_form':
            form_documento = DocumentoLaboralForm(request.POST, request.FILES)
            if form_documento.is_valid():

                # Obtener el archivo cargado
                archivo = request.FILES['documento']

                # Ruta de almacenamiento del archivo
                ruta = f'documentos/instructores/{usuario.perfil.nom}{usuario.perfil.apelli}{usuario.perfil.dni}/academico/{archivo.name}'
                ruta_guardada = default_storage.save(ruta, archivo)

                # Crear el registro en T_docu
                t_docu = T_docu.objects.create(
                    nom=archivo.name,
                    tipo=archivo.name.split('.')[-1],
                    tama=str(archivo.size // 1024) + " KB",  # Tamaño en KB
                    archi=ruta_guardada,
                    priva='No',  # O cualquier valor adecuado
                    esta='Activo'  # O cualquier estado inicial adecuado
                )

                # Guardar el formulario de DocumentoLaboralForm (sin guardar aún)
                documento = form_documento.save(commit=False)
                documento.usu = request.user  # Asociar el documento al usuario actual
                documento.esta = 'Cargado'  # Estado inicial del documento
                documento.docu = t_docu  # Asignar el documento de T_docu
                documento.tipo = 'academico'  # Asignar el documento de T_docu
                documento.save()  # Guardar el documento
                messages.success(request, "Documento guardado satisfactoriamente.")

                # Redirigir al perfil después de guardar
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                print(form_documento.errors)  # Imprimir errores para depuración
                messages.error(request, 'Por favor, corrige los errores en el formulario.')
        elif 'cv_file' in request.FILES:
            archivo = request.FILES['cv_file']

            # Ruta de almacenamiento del archivo
            ruta = f'documentos/instructores/{usuario.perfil.nom}{usuario.perfil.apelli}{usuario.perfil.dni}/HV/{archivo.name}'
            ruta_guardada = default_storage.save(ruta, archivo)

            # Crear el registro en T_docu
            t_docu = T_docu.objects.create(
                nom=archivo.name,
                tipo=archivo.name.split('.')[-1],
                tama=str(archivo.size // 1024) + " KB",  # Tamaño en KB
                archi=ruta_guardada,
                priva='No',  # O cualquier valor adecuado
                esta='Activo'  # O cualquier estado inicial adecuado
            )

            # Guardar el formulario de DocumentoLaboralForm (sin guardar aún)
            documento = form_documento.save(commit=False)
            documento.usu = request.user  # Asociar el documento al usuario actual
            documento.esta = 'Cargado'  # Estado inicial del documento
            documento.docu = t_docu  # Asignar el documento de T_docu
            documento.tipo = 'hv'  # Asignar el documento de T_docu
            documento.nom = 'Hoja de Vida'  # Asignar el documento de T_docu
            documento.cate = 'hv'  # Asignar el documento de T_docu
            documento.save()  # Guardar el documento
            messages.success(request, "Documento guardado satisfactoriamente.")

            # Redirigir al perfil después de guardar
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        elif request.POST.get('form_id') == 'perfil_form':  # Actualización de perfil
            form_perfil = PerfilForm(request.POST, instance=request.user.t_perfil)

            if form_perfil.is_valid():
                datos_actualizados = form_perfil.cleaned_data
                print(datos_actualizados)
                if 'fecha_naci' not in datos_actualizados or datos_actualizados['fecha_naci'] is None:
                    print("No viene fecha")
                    perfil_fe = T_perfil.objects.get(id = request.user.t_perfil.id)
                    form_perfil.instance.fecha_naci = perfil_fe.fecha_naci
                    print(form_perfil.instance.fecha_naci)
                form_perfil.save()
                messages.success(request, "Perfil actualizado correctamente.")
                return redirect('perfil')

                
            # Manejo del correo electrónico
            nuevo_email = request.POST.get('email')
            if nuevo_email:
                usuario_act = User.objects.get(id=request.user.id)
                usuario_act.email = nuevo_email
                usuario_act.save()
                perfil_act = T_perfil.objects.get(user=usuario_act)
                perfil_act.mail = nuevo_email
                perfil_act.save()

                request.user.refresh_from_db()
                #request.user.save()  # Guardar el nuevo correo en auth_user
                messages.success(request, "Correo electrónico actualizado correctamente.")
            
            return redirect('perfil')
        else:
            print(form_documento.errors)  # Imprimir errores para depuración
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            
        
    form_perfil = PerfilForm(instance=request.user.t_perfil)
    form_documento = DocumentoLaboralForm()
    form_contraseña = CustomPasswordChangeForm(user=request.user)
    return render(request, 'perfil.html', {
        'usuario': usuario,
        'form_contraseña': form_contraseña,
        'form_documento': form_documento,
        'documentos': documentos,
        'documentos_aca': documentos_aca,
        'hoja_vida': hoja_vida,
        'form_perfil': form_perfil
    })

def editar_perfil(request):
    perfil = getattr(request.user, 't_perfil', None)
    if request.method == 'POST':
        print("Si llega!")
        form = PerfilEForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = PerfilEForm(instance=perfil)  # Pre-poblar el formulario con los datos actuales del perfil
    return redirect(request.META.get('HTTP_REFERER', '/'))

def eliminar_documentoinstru(request, hv_id):
    archivo = get_object_or_404(T_docu_labo, id=hv_id)
    documento = get_object_or_404(T_docu, id=archivo.docu.id)
    mensaje = archivo.tipo
    if mensaje == 'laboral':
        mensaje = "Documento eliminado"
    elif mensaje == 'academico':
        mensaje = "Documento eliminado"
    elif mensaje == 'hv':
        mensaje = "Hoja de vida eliminada"
    
    archivo.delete()
    documento.delete()
    messages.success(request, mensaje)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_admin(request):
    perfil = getattr(request.user, 't_perfil', None)
    rol = perfil.rol
    return render(request, 'admin_dashboard.html', {'rol':rol})

### INSTRUCTORES ###

@login_required
def instructores(request):
    instructores = T_instru.objects.select_related('perfil').all()
    return render(request, 'instructor.html', {
        'instructores': instructores
    })

@login_required
def crear_instructor(request):

    if request.method == 'GET':

        user_form = UserFormCreate()
        perfil_form = PerfilForm()
        instructor_form = InstructorForm()

        return render(request, 'instructor_crear.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
            'instructor_form': instructor_form
        })
    else:
        try:
            user_form = UserFormCreate(request.POST)
            perfil_form = PerfilForm(request.POST)
            instructor_form = InstructorForm(request.POST)
            if user_form.is_valid() and perfil_form.is_valid() and instructor_form.is_valid():
                # Creacion del usuario
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()

                # creacion del perfil
                new_perfil = perfil_form.save(commit=False)
                new_perfil.user = new_user
                new_perfil.rol = 'instructor'
                new_perfil.mail = new_user.email
                new_perfil.save()

                # creacion del instructor
                new_instructor = instructor_form.save(commit=False)
                new_instructor.perfil = new_perfil
                new_instructor.save()
                return redirect('instructores')

        except ValueError as e:
            return render(request, 'crear_instructor.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'instructor_form': instructor_form,
                'error': f'Ocurrió un error: {str(e)}'
            })

@login_required
def instructor_detalle(request, instructor_id):
    instructor = get_object_or_404(T_instru, pk=instructor_id)
    perfil = instructor.perfil
    user = perfil.user

    if request.method == 'GET':
        user_form = UserFormEdit(instance=user)
        perfil_form = PerfilForm(instance=perfil)
        instructor_form = InstructorForm(instance=instructor)
        return render(request, 'instructor_detalle.html', {
            'instructor': instructor,
            'user_form': user_form,
            'perfil_form': perfil_form,
            'instructor_form': instructor_form
        })
    else:
        try:
            # Si se envía el formulario con los datos modificados
            user_form = UserFormEdit(request.POST, instance=user)
            perfil_form = PerfilForm(request.POST, instance=perfil)
            instructor_form = InstructorForm(request.POST, instance=instructor)
            if user_form.is_valid() and perfil_form.is_valid() and instructor_form.is_valid():
                user_form.save()
                perfil_form.save()
                instructor_form.save()
                # Redirigir a la lista de instructores (ajusta según sea necesario)
                return redirect('instructores')
        except ValueError:
            # Si ocurre un error al guardar, mostrar el formulario nuevamente con el mensaje de error
            return render(request, 'instructor_detalle.html', {
                'instructor': instructor,
                'user_form': user_form,
                'perfil_form': perfil_form,
                'instructor_form': instructor_form,
                'error': "Error al actualizar el instructor. Verifique los datos."})

@login_required
def instructor_detalle_tabla(request, instructor_id):
    try:
        instructor = get_object_or_404(T_instru, pk=instructor_id)
        instructor_data = model_to_dict(instructor)

        # Incluimos datos relacionados del perfil
        if hasattr(instructor, 'perfil'):
            perfil_data = model_to_dict(instructor.perfil)

            # Si el perfil tiene una relación con Usuario, la agregamos
            if hasattr(instructor.perfil, 'user'):
                perfil_data['user'] = {
                    'username': instructor.perfil.user.username,
                    'email': instructor.perfil.user.email,
                    'first_name': instructor.perfil.user.first_name,
                    'last_name': instructor.perfil.user.last_name,
                }

        instructor_data['perfil'] = perfil_data

        return JsonResponse({'info_adicional': instructor_data})
    except T_instru.DoesNotExist:
        return JsonResponse({'error': 'Registro no encontrado'}, status=404)

### CUENTAS ###

@login_required
def cuentas(request):
    cuentas = T_cuentas.objects.all()
    return render(request, 'cuentas.html', {
        'cuentas': cuentas
    })

@login_required
def crear_pcuentas(request):
    if request.method == 'GET':
        user_form = UserFormCreate()
        perfil_form = PerfilForm()

        return render(request, 'cuentas_crear.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
        })
    else:
        try:
            user_form = UserFormCreate(request.POST)
            perfil_form = PerfilForm(request.POST)

            if user_form.is_valid() and perfil_form.is_valid():
                username = user_form.cleaned_data['username']
                if User.objects.filter(username=username).exists():
                    return render(request, 'cuentas_crear.html', {
                        'user_form': user_form,
                        'perfil_form': perfil_form,
                        'error1': 'El usuario ya existe.'
                    })

                # Creación del usuario
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()

                # Creación del perfil
                new_perfil = perfil_form.save(commit=False)
                new_perfil.user = new_user
                new_perfil.rol = 'cuentas'
                new_perfil.mail = new_user.email
                new_perfil.save()

                # Creación del gestor
                new_cuentas = T_cuentas(
                    perfil = new_perfil,
                    esta = 'activo'
                )
                new_cuentas.save()

                return redirect('cuentas')

            else:
                return render(request, 'cuentas_crear.html', {
                    'user_form': user_form,
                    'perfil_form': perfil_form,
                    'error': 'Por favor corrige los errores en el formulario.'
                })

        except ValueError as e:
            return render(request, 'cuentas_crear.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'error': f'Error: {str(e)}'
            })

@login_required
def cuentas_detalle(request, cuentas_id):
    cuentas = get_object_or_404(T_cuentas, pk=cuentas_id)
    perfil = cuentas.perfil
    if request.method == 'GET':
        perfil_form = PerfilEditForm(instance=perfil)
        return render(request, 'cuentas_detalle.html', {
            'cuentas': cuentas,
            'perfil_form': perfil_form,
        })
    elif request.method == 'POST':
        perfil_form = PerfilEditForm(request.POST, instance=perfil)
        if perfil_form.is_valid() :
            perfil_form.save()
            return redirect('cuentas')
        return render(request, 'cuentas_detalle.html', {
            'cuentas': cuentas,
            'perfil_form': perfil_form,
        })

### REP. LEGAL ###

@login_required
def representante_legal(request):
    representantes_legales = T_repre_legal.objects.all()
    return render(request, 'representantesLegales.html', {
        'representantesLegales': representantes_legales
    })

@login_required  # Funcion para crear Representante legal
def crear_representante_legal(request):
    if request.method == 'GET':

        replegal_form = RepresanteLegalForm()
        return render(request, 'representanteLegal_crear.html', {
            'replegal_form': replegal_form
        })
    else:
        try:
            replegal_form = RepresanteLegalForm(request.POST)
            if replegal_form.is_valid():
                new_represanteLegal = replegal_form.save(commit=False)
                new_represanteLegal.save()
                return redirect('represantesLegales')
        except ValueError as e:
            return render(request, 'representanteLegal_crear.html', {
                'replegal_form': replegal_form,
                'error': f'Ocurrió un error: {str(e)}'
            })

@login_required  # Funcion para Actualizar Representante legal
def detalle_representante_legal(request, repreLegal_id):
    representante_legal = get_object_or_404(T_repre_legal, id=repreLegal_id)

    if request.method == 'GET':

        replegal_form = RepresanteLegalForm(instance=representante_legal)
        return render(request, 'representanteLegal_detalle.html', {
            'represante_legal': representante_legal,
            'replegal_form': replegal_form
        })
    else:
        try:
            replegal_form = RepresanteLegalForm(
                request.POST, instance=representante_legal)
            if replegal_form.is_valid():
                replegal_form.save()
                return redirect('represantesLegales')
        except ValueError:
            return render(request, 'representanteLegal_detalle.html', {
                'replegal_form': replegal_form,
                'error': 'Error al actualizar el administrador. Verifique los datos'
            })

@login_required  # Funcion para eliminar  Representante legal
def eliminar_representante_legal(request, repreLegal_id):
    representante_legal = get_object_or_404(T_repre_legal, id=repreLegal_id)
    if request.method == 'POST':
        representante_legal.delete()
        return redirect('represantesLegales')
    return render(request, 'confirmar_eliminacion_represante_legal.html', {
        'represante_legal': representante_legal,
    })

 ### APRENDICES ###

@login_required
def aprendices(request):
    perfil = getattr(request.user, 't_perfil', None)
    rol = perfil.rol
    aprendices = T_apre.objects.select_related('perfil__user').all()
    return render(request, 'aprendiz.html', {
        'aprendices': aprendices,
        'rol': rol
    })

@login_required
def crear_aprendices(request):  # Funcion para crear aprendiz
    if request.method == 'GET':

        user_form = UserFormCreate()
        perfil_form = PerfilForm()
        aprendiz_form = AprendizForm()

        return render(request, 'aprendiz_crear.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
            'aprendiz_form': aprendiz_form
        })
    else:
        try:
            user_form = UserFormCreate(request.POST)
            perfil_form = PerfilForm(request.POST)
            aprendiz_form = AprendizForm(request.POST)
            if user_form.is_valid() and perfil_form.is_valid() and aprendiz_form.is_valid():
                # Creacion del usuario
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()

                # creacion del perfil
                new_perfil = perfil_form.save(commit=False)
                new_perfil.user = new_user
                new_perfil.rol = 'aprendiz'
                new_perfil.mail = new_user.email
                new_perfil.save()

                # creacion del aprendiz
                new_aprendiz = aprendiz_form.save(commit=False)
                new_aprendiz.perfil = new_perfil
                new_aprendiz.save()
                return redirect('aprendices')

        except ValueError as e:
            return render(request, 'aprendiz_crear.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'aprendiz_form': aprendiz_form,
                'error': f'Ocurrió un error: {str(e)}'
            })

@login_required
def detalle_aprendices(request, aprendiz_id):  # Funcion para editar aprendiz
    aprendiz = get_object_or_404(T_apre, pk=aprendiz_id)
    perfil = aprendiz.perfil
    user = perfil.user

    if request.method == 'GET':

        user_form = UserFormCreate(instance=user)
        perfil_form = PerfilForm(instance=perfil)
        aprendiz_form = AprendizForm(instance=aprendiz)

        return render(request, 'aprendiz_detalle.html', {
            'aprendiz': aprendiz,
            'user_form': user_form,
            'perfil_form': perfil_form,
            'aprendiz_form': aprendiz_form
        })
    else:
        try:
            user_form = UserFormCreate(request.POST)
            perfil_form = PerfilForm(request.POST)
            aprendiz_form = AprendizForm(request.POST)
            if user_form.is_valid() and perfil_form.is_valid() and aprendiz_form.is_valid():
                user_form.save()
                perfil_form.save()
                aprendiz_form.save()
            return redirect('aprendices')

        except ValueError:
            return render(request, 'aprendiz_detalle.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'aprendiz_form': aprendiz_form,
                'error': 'Error al actualizar el administrador. Verifique los datos'
            })

@login_required
def eliminar_aprendiz(request, aprendiz_id):  # funcion para eliminar aprendiz

    aprendiz = get_object_or_404(T_apre, pk=aprendiz_id)

    if request.method == 'POST':
        aprendiz.delete()
        return redirect('aprendices')
    return render(request, '', {'aprendiz': aprendiz})

### LIDERES ###

@login_required
def lideres(request):
    lideres = T_lider.objects.select_related('perfil__user').all()
    return render(request, 'lideres.html', {
        'lideres': lideres
    })

@login_required  # Funcion para crear lider
def crear_lideres(request):

    if request.method == 'GET':
        user_form = UserFormCreate()
        perfil_form = PerfilForm()
        lider_form = LiderForm()
        return render(request, 'lider_crear.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
            'lider_form': lider_form
        })
    else:
        try:
            # Si se envía el formulario con los datos modificados
            user_form = UserFormCreate(request.POST)
            perfil_form = PerfilForm(request.POST)
            lider_form = LiderForm(request.POST)
            if user_form.is_valid() and perfil_form.is_valid() and lider_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                new_perfil = perfil_form.save(commit=False)
                new_perfil.user = new_user
                new_perfil.rol = 'lider'
                new_perfil.save()
                new_lider = lider_form.save(commit=False)
                new_lider.perfil = new_perfil
                new_lider.save()
                return redirect('lideres')
            else:
                # Manejo de formularios inválidos
                return render(request, 'lider_crear.html', {
                    'user_form': user_form,
                    'perfil_form': perfil_form,
                    'lider_form':  lider_form,
                    'error': "Datos inválidos en el formulario. Corrige los errores."
                })
        except ValueError:
            # Si ocurre un error al guardar, mostrar el formulario nuevamente con el mensaje de error
            return render(request, 'lider_crear.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'lider_form': lider_form,
                'error': "Se presenta un error al crear el lider"})


@login_required  # Funcion para actualizar informacion de lider
def detalle_lideres(request, lider_id):
    lider = get_object_or_404(T_lider, id=lider_id)
    perfil = lider.perfil
    user = perfil.user

    if request.method == 'GET':
        user_form = UserFormEdit(instance=user)
        perfil_form = PerfilForm(instance=perfil)
        lider_form = LiderForm(instance=lider)
        return render(request, 'lider_detalle.html', {
            'lider': lider,
            'user_form': user_form,
            'perfil_form': perfil_form,
            'lider_form': lider_form
        })
    else:
        try:
            # Si se envía el formulario con los datos modificados
            user_form = UserFormEdit(request.POST, instance=user)
            perfil_form = PerfilForm(request.POST, instance=perfil)
            lider_form = LiderForm(request.POST, instance=lider)
            if user_form.is_valid() and perfil_form.is_valid() and lider_form.is_valid():

                user_form.save()
                perfil_form.save()
                lider_form.save()
                return redirect('lideres')

        except ValueError:
            # Si ocurre un error al guardar, mostrar el formulario nuevamente con el mensaje de error
            return render(request, 'lider_detalle.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'lider_form': lider_form,
                'error': "Error al actualizar el lider. Verifique los datos."})


@login_required
def eliminar_lideres(request, lider_id):  # Funcion para eliminar informacion de lider
    lider = get_object_or_404(T_lider, id=lider_id)
    if request.method == 'POST':
        lider.delete()
        return redirect('lideres')
    return render(request, 'confirmar_eliminacion_lider.html', {
        'lider': lider
    })

### ADMINISTRADOR ###


@login_required
def administradores(request):
    administradores = T_admin.objects.select_related('perfil__user').all()
    return render(request, 'administradores.html', {
        'administradores': administradores
    })


@login_required
def crear_administradores(request):  # funcion para crear administradores

    if request.method == 'GET':
        user_form = UserFormCreate()
        perfil_form = PerfilForm()
        admin_form = AdministradoresForm()

        return render(request, 'administradores_crear.html', {
            'admin_form': admin_form,
            'perfil_form': perfil_form,
            'user_form':  user_form
        })
    else:
        try:
            # Si se envía el formulario con los datos modificados
            user_form = UserFormCreate(request.POST)
            perfil_form = PerfilForm(request.POST)
            admin_form = AdministradoresForm(request.POST)
            if user_form.is_valid() and perfil_form.is_valid() and admin_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                new_perfil = perfil_form.save(commit=False)
                new_perfil.user = new_user
                new_perfil.rol = 'admin'
                new_perfil.save()
                new_admin = admin_form.save(commit=False)
                new_admin.perfil = new_perfil
                new_admin.save()
                return redirect('administradores')
            else:
                # Manejo de formularios inválidos
                return render(request, 'administradores_crear.html', {
                    'user_form': user_form,
                    'perfil_form': perfil_form,
                    'admin_form': admin_form,
                    'error': "Datos inválidos en el formulario. Corrige los errores."
                })
        except ValueError:
            # Si ocurre un error al guardar, mostrar el formulario nuevamente con el mensaje de error
            return render(request, 'administradores_crear.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'admin_form': admin_form,
                'error': "Error al actualizar el administrador. Verifique los datos."})


@login_required
# funcion para actualizar informacion de los administradores
def detalle_administradores(request, admin_id):
    administrador = get_object_or_404(T_admin, id=admin_id)
    perfil = administrador.perfil
    user = perfil.user

    if request.method == 'GET':
        user_form = UserFormEdit(instance=user)
        perfil_form = PerfilForm(instance=perfil)
        admin_form = AdministradoresForm(instance=administrador)

        return render(request, 'administradores_detalle.html', {
            'administrador': administrador,
            'admin_form': admin_form,
            'perfil_form': perfil_form,
            'user_form':  user_form
        })
    else:
        try:
            # Si se envía el formulario con los datos modificados
            user_form = UserFormEdit(request.POST, instance=user)
            perfil_form = PerfilForm(request.POST, instance=perfil)
            admin_form = AdministradoresForm(
                request.POST, instance=administrador)
            if user_form.is_valid() and perfil_form.is_valid() and admin_form.is_valid():
                user_form.save()
                perfil_form.save()
                admin_form.save()

                # Redirigir a la lista de administradores (ajusta según sea necesario)
                return redirect('administradores')
        except ValueError:
            # Si ocurre un error al guardar, mostrar el formulario nuevamente con el mensaje de error
            return render(request, 'administradores_detalle.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'admin_form': admin_form,
                'error': "Error al actualizar el administrador. Verifique los datos."})


@login_required
def eliminar_admin(request, admin_id):  # Funcion para eliminar informacion del admin
    admin = get_object_or_404(T_admin, pk=admin_id)
    if request.method == 'POST':
        admin.delete()
        return redirect('administradores')
    return render(request, 'confirmar_eliminacion_administradores.html', {'admin': admin})


@login_required
def administrador_detalle_tabla(request, admin_id):
    try:
        administrador = get_object_or_404(T_admin, id=admin_id)
        administrador_data = model_to_dict(administrador)

        # Incluimos datos relacionados del perfil
        if hasattr(administrador, 'perfil'):
            administrador_data = model_to_dict(administrador.perfil)

            # Si el perfil tiene una relación con Usuario, la agregamos
            if hasattr(administrador.perfil, 'user'):
                administrador_data['user'] = {
                    'username': administrador.perfil.user.username,
                    'email': administrador.perfil.user.email,
                    'first_name': administrador.perfil.user.first_name,
                    'last_name': administrador.perfil.user.last_name,
                }

        administrador_data['perfil'] = administrador_data

        return JsonResponse({'info_adicional': administrador_data})
    except T_instru.DoesNotExist:
        return JsonResponse({'error': 'Registro no encontrado'}, status=404)

### NOVEDADES ###


@login_required
def novedades(request):
    novedades = T_nove.objects.all()
    return render(request, 'novedades.html', {
        'novedades': novedades
    })


@login_required
def crear_novedad(request):

    if request.method == 'GET':

        novedad_form = NovedadForm()

        return render(request, 'novedad_crear.html', {
            'novedad_form': novedad_form
        })
    else:
        try:
            novedad_form = NovedadForm(request.POST)
            if novedad_form.is_valid():
                # Creacion de la novedad
                new_novedad = novedad_form.save(commit=False)
                new_novedad.estado = 'creado'
                new_novedad.save()
                return redirect('novedades')

        except ValueError as e:
            return render(request, 'novedad_crear.html', {
                'novedad_form': novedad_form,
                'error': f'Ocurrió un error: {str(e)}'
            })


## DEPARTAMENTOS ##
@login_required
def departamentos(request):
    departamentos = T_departa.objects.all()
    return render(request, 'departamentos.html', {
        'departamentos': departamentos
    })


@login_required
def creardepartamentos(request):  # funcion para crear departamento
    if request.method == 'GET':
        departamentosForm = DepartamentoForm()
        return render(request, 'departamentos_crear.html', {
            'departamentosForm': departamentosForm
        })
    else:
        try:
            departamentosForm = DepartamentoForm(request.POST)
            if departamentosForm.is_valid():
                new_departamento = departamentosForm.save(commit=False)
                new_departamento.save()
                return redirect('departamentos')
        except ValueError:
            return render(request, 'departamentos_crear.html', {
                'departamentosForm': departamentosForm,
                'error': '"Error al crear departamento. Verifique los datos.'
            })


@login_required
# funcion para actualizar info departamento
def detalle_departamentos(request, departamento_id):
    departamentos = get_object_or_404(T_departa, id=departamento_id)
    if request.method == 'GET':
        departamentosForm = DepartamentoForm(instance=departamentos)
        return render(request, 'departamentos_detalle.html', {
            'departamentos': departamentos,
            'departamentosForm': departamentosForm
        })
    else:
        try:
            departamentosForm = DepartamentoForm(
                request.POST, instance=departamentos)
            if departamentosForm.is_valid():
                departamentosForm.save()
                return redirect('departamentos')
        except ValueError:
            return render(request, 'departamentos_detalle.html', {
                'departamentosForm': departamentosForm,
                'error': '"Error al actualizar departamento. Verifique los datos.'
            })


def eliminar_departamentos(request, departamento_id):
    departamento = get_object_or_404(T_departa, id=departamento_id)
    if request.method == 'POST':
        departamento.delete()
        return redirect('departamentos')
    return render(request, 'confirmar_eliminacion_departamento.html', {
        'departamento': departamento,
    })


## MUNICIPIOS ##
def municipios(request):
    municipios = T_munici.objects.all()
    return render(request, 'municipios.html', {
        'municipios': municipios
    })


@login_required
def crearmunicipios(request):  # funcion para crear municipio
    if request.method == 'GET':
        municipiosForm = MunicipioForm()
        return render(request, 'municipios_crear.html', {
            'municipiosForm': municipiosForm
        })
    else:
        try:
            municipiosForm = MunicipioForm(request.POST)
            if municipiosForm.is_valid():
                new_municipio = municipiosForm.save(commit=False)
                new_municipio.save()
                return redirect('municipios')
        except ValueError:
            return render(request, 'municipios_crear.html', {
                'municipiosForm': municipiosForm,
                'error': 'Error al al crear municipio. Verifique los datos.'
            })


@login_required
def detalle_municipios(request, municipio_id):  # funcion para editar municipio
    municipios = get_object_or_404(T_munici, id=municipio_id)

    if request.method == 'GET':
        municipiosForm = MunicipioForm(instance=municipios)
        return render(request, 'municipios_detalle.html', {
            'municipios': municipios,
            'municipiosForm': municipiosForm
        })
    else:
        try:
            municipiosForm = MunicipioForm(request.POST, instance=municipios)
            if municipiosForm.is_valid():
                municipiosForm.save()
                return redirect('municipios')
        except ValueError:
            return render(request, 'municipios_detalle.html', {
                'municipiosForm': municipiosForm,
                'error': 'Error al actualizar. Verifique los datos.'
            })


def eliminar_municipios(request, municipio_id):  # funcion para eliminar municipio
    municipio = get_object_or_404(T_munici, id=municipio_id)

    if request.method == 'POST':
        municipio.delete()
        return redirect('municipios')
    return render(request, 'confirmar_eliminacion_municipio.html', {
        'municipio': municipio,
    })


## Instituciones ##
@login_required
def instituciones(request):
    instituciones = T_insti_edu.objects.all()
    return render(request, 'instituciones.html', {
        'instituciones': instituciones
    })


@login_required
def crear_instituciones(request):  # Función para crear institución
    if request.method == 'GET':
        institucionForm = InstitucionForm()
        return render(request, 'instituciones_crear.html', {
            'institucionForm': institucionForm
        })

    elif request.method == 'POST':
        try:
            institucionForm = InstitucionForm(request.POST)
            
            # Validar el formulario
            if institucionForm.is_valid():
                # Obtener el departamento seleccionado
                departamento_id = institucionForm.cleaned_data.get('depa')
                
                # Actualizar el queryset de municipios
                if departamento_id:
                    institucionForm.fields['muni'].queryset = T_munici.objects.filter(nom_departa=departamento_id)
                

                # Guardar la nueva institución
                new_institucion = institucionForm.save(commit=False)
                new_institucion.vigen = datetime.now().year
                new_institucion.save()
                return redirect('instituciones')  # Redirigir a la lista de instituciones
            
            # Si el formulario no es válido, renderizar con errores
            return render(request, 'instituciones_crear.html', {
                'institucionForm': institucionForm,
                'error': 'Error al crear institución. Verifique los datos ingresados.'
            })
        
        except ValueError:
            # Manejar errores específicos
            return render(request, 'instituciones_crear.html', {
                'institucionForm': institucionForm,
                'error': 'Error al crear institución. Verifique los datos ingresados.'
            })

    else:
        # Si el método no es GET ni POST, redirigir
        return redirect('instituciones')



@login_required
# funcion para actualizar institucion
def detalle_instituciones(request, institucion_id):
    institucion = get_object_or_404(T_insti_edu, id=institucion_id)

    if request.method == 'GET':
        institucionForm = InstitucionForm(instance=institucion)
        return render(request, 'instituciones_detalle.html', {
            'institucion': institucion,
            'institucionForm': institucionForm
        })
    else:
        try:
            institucionForm = InstitucionForm(
                request.POST, instance=institucion)
            if institucionForm.is_valid():
                institucionForm.save()
                return redirect('instituciones')
        except ValueError:
            return render(request, 'instituciones_detalle.html', {
                'institucionForm': institucionForm,
                'error': 'Error al actualizar. Verifique los datos.'
            })


@login_required  # funcion para eliminar institucion
def eliminar_instituciones(request, institucion_id):
    institucion = get_object_or_404(T_insti_edu, id=institucion_id)

    if request.method == 'POST':
        institucion.delete()
        return redirect('instituciones')
    return render(request, 'confirmar_eliminacion_instituciones.html', {
        'institucion': institucion,
    })


## Centros de formacion ##
@login_required
def centrosformacion(request):
    centrosformacion = T_centro_forma.objects.all()
    return render(request, 'centro_formacion.html', {
        'centrosformacion': centrosformacion
    })


login_required  # Funcion para crear centros de formacion


def crear_centrosformacion(request):
    if request.method == 'GET':
        centrosformacionForm = CentroFormacionForm()
        return render(request, 'centro_formacion_crear.html', {
            'centrosformacionForm': centrosformacionForm
        })
    else:
        try:
            centrosformacionForm = CentroFormacionForm(request.POST)
            if centrosformacionForm.is_valid():
                new_centroFormacion = centrosformacionForm.save(commit=False)
                new_centroFormacion.save()
                return redirect('centrosformacion')
        except ValueError:
            return render(request, 'centro_formacion_crear.html', {
                'centrosformacionForm': centrosformacionForm,
                'error': 'Error al crear institución. Verifique los datos'
            })


@login_required  # funcion para actualizar centro de formacion
def detalle_centrosformacion(request, centroformacion_id):
    centroFormacion = get_object_or_404(T_centro_forma, id=centroformacion_id)

    if request.method == 'GET':
        centrosformacionForm = CentroFormacionForm(instance=centroFormacion)
        return render(request, 'centro_formacion_detalle.html', {
            'centroFormacion': centroFormacion,
            'centrosformacionForm': centrosformacionForm
        })
    else:
        try:
            centrosformacionForm = CentroFormacionForm(
                request.POST, instance=centroFormacion)
            if centrosformacionForm.is_valid():
                centrosformacionForm.save()
                return redirect('centrosformacion')
        except ValueError:
            return render(request, 'centro_formacion_detalle.html', {
                'centrosformacionForm': centrosformacionForm,
                'error': 'Error al crear institución. Verifique los datos'
            })


@login_required  # funcion para eliminar centro de formacion
def eliminar_centrosformacion(request, centroformacion_id):
    centroformacion = get_object_or_404(T_centro_forma, id=centroformacion_id)

    if request.method == 'POST':
        centroformacion.delete()
        return redirect('centrosformacion')
    return render(request, 'confirmar_eliminacion_centro_formacion.html', {
        'centroformacion': centroformacion,
    })

def obtener_municipios(request):
    departamento_id = request.GET.get('departamento_id')
    if departamento_id:
        municipios = T_munici.objects.filter(nom_departa_id=departamento_id).values('id', 'nom_munici')
        return JsonResponse(list(municipios), safe=False)
    return JsonResponse({'error': 'No se proporcionó el ID del departamento'}, status=400)

# Función para generar contraseña aleatoria
def generar_contraseña(length=8):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(length))

@login_required
def cargar_aprendices_masivo(request):
    if request.method == 'POST':
        form = CargarAprendicesMasivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            datos_csv = TextIOWrapper(archivo.file, encoding='utf-8-sig')

            # Convertir punto y coma a coma en caso de que el CSV use el delimitador ";"
            contenido_csv = datos_csv.read().replace(';', ',')

            # Leer el archivo CSV
            lector = csv.DictReader(contenido_csv.splitlines())

            errores = []
            resumen = {
                "insertados": 0,
                "errores": 0,
                "duplicados_dni": []
            }

            try:
                # Iniciar una transacción
                with transaction.atomic():
                    representantes = {}  # Diccionario para llevar un registro de los representantes procesados

                    for fila in lector:
                        try:
                            # Validar campos

                            if 'email' not in fila or not fila['email']:
                                errores.append(f"Error: 'email' ausente o vacío en la fila: {fila}")
                                resumen["errores"] += 1
                                continue
                            
                            if 'nom' not in fila or not fila['nom']:
                                errores.append(f"Error: 'nombre' ausente o vacío en la fila: {fila}")
                                resumen["errores"] += 1
                                continue

                            if 'dni' not in fila or not fila['dni']:
                                errores.append(f"Error: 'dni' ausente o vacío en la fila: {fila}")
                                resumen["errores"] += 1
                                continue
                            
                            # Verificar si el DNI ya existe
                            dni = fila['dni']
                            if T_perfil.objects.filter(dni=dni).exists():
                                mensaje_error = f"El DNI '{dni}' ya está registrado en el sistema. Fila omitida: {fila}"
                                errores.append(mensaje_error)  # Registrar el error en la lista
                                resumen["duplicados_dni"].append(dni)
                                resumen["errores"] += 1
                                continue

                            # Validar email
                            try:
                                user_email = fila['email']
                                if not user_email:
                                    raise ValidationError("El correo es inválido")
                            except ValidationError as e:
                                errores.append(f"Error: Correo inválido en la fila {fila}: {e}")
                                resumen["errores"] += 1
                                continue
                            
                            # Convertir la fecha de nacimiento si existe
                            fecha_naci_str = fila.get('fecha_naci', '').strip()
                            if fecha_naci_str:
                                try:
                                    # Intentar convertir la fecha en formato "1/01/1980"
                                    fecha_naci = datetime.strptime(fecha_naci_str, '%d/%m/%Y')
                                    # Convertirla al formato YYYY-MM-DD
                                    fecha_naci = fecha_naci.strftime('%Y-%m-%d')
                                except ValueError:
                                    errores.append(f"Error: La fecha de nacimiento '{fecha_naci_str}' no tiene el formato correcto en la fila: {fila}")
                                    resumen["errores"] += 1
                                    continue
                            else:
                                fecha_naci = None

                            # Generar un username único basado en el nombre y apellido
                            base_username = (fila['nom'][:3] + fila['apelli'][:3]).lower()  # Tomamos los primeros 3 caracteres del nombre y apellido
                            username = base_username
                            i = 1

                            # Verificar que el username no exista
                            while User.objects.filter(username=username).exists():
                                username = f"{base_username}{i}"
                                i += 1

                            # Generar contraseña aleatoria
                            contraseña = generar_contraseña()

                            # Crear el usuario
                            user = User.objects.create_user(
                                username=username,
                                password=contraseña,
                                email=fila['email']
                            )
                            
                            # Crear el perfil
                            perfil = T_perfil.objects.create(
                                user=user,
                                nom=fila['nom'],
                                apelli=fila['apelli'],
                                tipo_dni=fila['tipo_dni'],
                                dni=dni,
                                tele=fila['tele'],
                                dire=fila['dire'],
                                gene=fila['gene'],
                                mail=fila['mail'],
                                fecha_naci=fecha_naci,  # Asignar la fecha ya convertida
                                rol="aprendiz"
                            )

                            # Verificar si el representante legal ya existe
                            nombre_repre = fila['nom_repre']
                            telefono_repre = fila['tele_repre']
                            repre_legal = representantes.get((nombre_repre, telefono_repre))

                            if not repre_legal:
                                # Si no existe, buscar en la base de datos
                                repre_legal = T_repre_legal.objects.filter(
                                    nom=nombre_repre,
                                    tele=telefono_repre
                                ).first()

                                if not repre_legal:
                                    # Si no existe en la base de datos, crear uno nuevo
                                    repre_legal = T_repre_legal.objects.create(
                                        nom=nombre_repre,
                                        tele=telefono_repre,
                                        dire=fila['dire_repre'],
                                        mail=fila['mail_repre'],
                                        paren=fila['parentezco']
                                    )
                                    
                                # Registrar el representante en el diccionario para evitar duplicados
                                representantes[(nombre_repre, telefono_repre)] = repre_legal

                            # Crear el aprendiz
                            aprendiz = T_apre.objects.create(
                                cod="z",
                                esta="Activo",
                                perfil=perfil,
                                repre_legal=repre_legal
                            )

                            # Enviar el correo con la contraseña
                            asunto = "Bienvenido a la plataforma"
                            mensaje = f"Hola {fila['nom']} {fila['apelli']},\n\nTu cuenta ha sido creada con éxito. A continuación se encuentran tus credenciales:\n\nUsuario: {username}\nContraseña: {contraseña}\n\nRecuerda cambiar tu contraseña después de iniciar sesión."
                            send_mail(
                                asunto,
                                mensaje,
                                settings.DEFAULT_FROM_EMAIL,
                                [fila['email']],
                                fail_silently=False,
                            )

                            resumen["insertados"] += 1

                        except Exception as e:
                            # En caso de error, revertir la transacción completa
                            errores.append(f"Error inesperado al procesar la fila {fila}: {str(e)}")
                            resumen["errores"] += 1
                            raise  # Lanza la excepción para que se revierta la transacción

            except Exception as e:
                # Si hay un error, todo lo insertado hasta ese momento se revertirá
                errores.append(f"Error en el proceso de importación: {str(e)}")
                resumen["errores"] = len(errores)

            # Resumen de los datos procesados
            return render(request, 'aprendiz_masivo_crear.html', {
                'form': form,
                'errores': errores,
                'resumen': resumen
            })

    else:
        form = CargarAprendicesMasivoForm()

    return render(request, 'aprendiz_masivo_crear.html', {'form': form})



class DataTablePagination(PageNumberPagination):
    page_size_query_param = 'length'  # Usado por DataTables
    page_query_param = 'start'       # Usado por DataTables
    page_size = 10                   # Tamaño por defecto si no se especifica

    def get_page_size(self, request):
        return int(request.query_params.get('length', self.page_size))

class T_insti_edu_APIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtén los parámetros que envía DataTables
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Consulta inicial
        queryset = T_insti_edu.objects.all()

        # Aplicar búsqueda si existe un término
        if search_value:
            queryset = queryset.filter(
                Q(nom__icontains=search_value) |
                Q(dire__icontains=search_value) |
                Q(muni__nom_munici__icontains=search_value) |
                Q(muni__nom_departa__nom_departa__icontains=search_value) |
                Q(secto__icontains=search_value) |
                Q(esta__icontains=search_value) |
                Q(dane__icontains=search_value) |
                Q(gene__icontains=search_value) |
                Q(zona__icontains=search_value)
            )

        # Total de registros
        total = queryset.count()

        # Total de registros después del filtro
        total_filtered = queryset.count()

        # Paginación
        queryset = queryset[start:start + length]

        # Serializa los datos
        serializer = T_insti_edu_Serializer(queryset, many=True)

        # Respuesta en el formato que espera DataTables
        return Response({
            'draw': draw,
            'recordsTotal': total,
            'recordsFiltered': total,  # Ajusta si aplicas filtros
            'data': serializer.data,
        })

@login_required
def gestores(request):
    # Obtén todos los gestores junto con sus departamentos asociados
    gestores = T_gestor.objects.prefetch_related(
        Prefetch(
            't_gestor_depa_set',  # Nombre del related_name entre gestor y gestor-depa
            queryset=T_gestor_depa.objects.select_related('depa')
        )
    )

    # Añade un atributo personalizado para concatenar los departamentos
    for gestor in gestores:
        gestor.departamentos = ', '.join(
            [depa.depa.nom_departa for depa in gestor.t_gestor_depa_set.all()]
        )

    return render(request, 'gestores.html', {
        'gestores': gestores
    })

@login_required
def crear_gestor(request):
    if request.method == 'GET':
        user_form = UserFormCreate()
        perfil_form = PerfilForm()
        gestor_depa_form = GestorDepaForm()

        return render(request, 'gestor_crear.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
            'gestor_depa_form': gestor_depa_form
        })
    else:
        try:
            user_form = UserFormCreate(request.POST)
            perfil_form = PerfilForm(request.POST)
            gestor_depa_form = GestorDepaForm(request.POST)

            if user_form.is_valid() and perfil_form.is_valid() and gestor_depa_form.is_valid():
                username = user_form.cleaned_data['username']
                if User.objects.filter(username=username).exists():
                    return render(request, 'gestor_crear.html', {
                        'user_form': user_form,
                        'perfil_form': perfil_form,
                        'gestor_depa_form': gestor_depa_form,
                        'error1': 'El usuario ya existe.'
                    })

                # Creación del usuario
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()

                # Creación del perfil
                new_perfil = perfil_form.save(commit=False)
                new_perfil.user = new_user
                new_perfil.rol = 'gestor'
                new_perfil.mail = new_user.email
                new_perfil.save()

                # Creación del gestor
                new_gestor = T_gestor(
                    perfil = new_perfil,
                    esta = 'asignado'
                )
                new_gestor.save()

                # Creacion de la relacion con departamento
                departamentos = gestor_depa_form.cleaned_data['departamentos']
                for departamento in departamentos:
                    departai = T_departa.objects.get(nom_departa=departamento)
                    new_gestor_depa = T_gestor_depa(
                        gestor = new_gestor,
                        depa = departai,
                        fecha_crea = datetime.now(),
                        usuario_crea = request.user
                    )
                    new_gestor_depa.save()
                
                return redirect('gestores')

            else:
                return render(request, 'gestor_crear.html', {
                    'user_form': user_form,
                    'perfil_form': perfil_form,
                    'gestor_depa_form': gestor_depa_form,
                    'error': 'Por favor corrige los errores en el formulario.'
                })

        except ValueError as e:
            return render(request, 'gestor_crear.html', {
                'user_form': user_form,
                'perfil_form': perfil_form,
                'gestor_depa_form': gestor_depa_form,
                'error': f'Error: {str(e)}'
            })
        
@login_required
def gestor_detalle(request, gestor_id):
    gestor = get_object_or_404(T_gestor, pk=gestor_id)
    perfil = gestor.perfil
    user = perfil.user

    if request.method == 'GET':
        perfil_form = PerfilEditForm(instance=perfil)

        # Seleccionar los departamentos asociados al gestor
        departamentos_asignados = T_gestor_depa.objects.filter(gestor=gestor).values_list('depa', flat=True)
        gestor_depa_form = GestorDepaForm(
            initial={'departamentos': departamentos_asignados}
        )

        return render(request, 'gestor_detalle.html', {
            'gestor': gestor,
            'perfil_form': perfil_form,
            'gestor_depa_form': gestor_depa_form
        })
    elif request.method == 'POST':
        perfil_form = PerfilEditForm(request.POST, instance=perfil)
        gestor_depa_form = GestorDepaForm(request.POST)

        if perfil_form.is_valid() and gestor_depa_form.is_valid():
            perfil_form.save()

            # Actualizar departamentos asociados
            nuevos_departamentos = gestor_depa_form.cleaned_data['departamentos']
            T_gestor_depa.objects.filter(gestor=gestor).delete()  # Elimina los existentes
            for depa in nuevos_departamentos:
                T_gestor_depa.objects.create(
                    gestor=gestor, 
                    depa=depa, 
                    fecha_crea = datetime.now(),
                    usuario_crea = request.user
                )

            return redirect('gestores')

        return render(request, 'gestor_detalle.html', {
            'gestor': gestor,
            'perfil_form': perfil_form,
            'gestor_depa_form': gestor_depa_form,
        })

# @login_required
# def instructor_detalle(request, instructor_id):
#     instructor = get_object_or_404(T_instru, pk=instructor_id)
#     perfil = instructor.perfil
#     user = perfil.user

#     if request.method == 'GET':
#         user_form = UserFormEdit(instance=user)
#         perfil_form = PerfilForm(instance=perfil)
#         instructor_form = InstructorForm(instance=instructor)
#         return render(request, 'instructor_detalle.html', {
#             'instructor': instructor,
#             'user_form': user_form,
#             'perfil_form': perfil_form,
#             'instructor_form': instructor_form
#         })
#     else:
#         try:
#             # Si se envía el formulario con los datos modificados
#             user_form = UserFormEdit(request.POST, instance=user)
#             perfil_form = PerfilForm(request.POST, instance=perfil)
#             instructor_form = InstructorForm(request.POST, instance=instructor)
#             if user_form.is_valid() and perfil_form.is_valid() and instructor_form.is_valid():
#                 user_form.save()
#                 perfil_form.save()
#                 instructor_form.save()
#                 # Redirigir a la lista de instructores (ajusta según sea necesario)
#                 return redirect('instructores')
#         except ValueError:
#             # Si ocurre un error al guardar, mostrar el formulario nuevamente con el mensaje de error
#             return render(request, 'instructor_detalle.html', {
#                 'instructor': instructor,
#                 'user_form': user_form,
#                 'perfil_form': perfil_form,
#                 'instructor_form': instructor_form,
#                 'error': "Error al actualizar el instructor. Verifique los datos."})
