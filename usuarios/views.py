from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from commons.models import T_instru, T_apre,T_perfil, T_admin, T_lider, T_nove, T_repre_legal, T_munici, T_departa, T_insti_edu, T_centro_forma
from .forms import InstructorForm,CargarAprendicesMasivoForm, UserFormCreate, UserFormEdit, PerfilForm, NovedadForm, AdministradoresForm, AprendizForm, LiderForm, RepresanteLegalForm, DepartamentoForm, MunicipioForm, InstitucionForm, CentroFormacionForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from io import TextIOWrapper
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import csv
import random
import string


# Create your views here.


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
            except T_perfil.DoesNotExist:
                pass  # Si no se encuentra el perfil, no hacer nada adicional

            # Si no es aprendiz, redirigir a novedades
            return redirect('novedades')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "El usuario ya existe"
                })
    return render(request, 'signup.html', {
        'form': UserCreationForm,
        'error': "Las contraseñas no coinciden"
    })


@login_required
def signout(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_admin(request):
    return render(request, 'admin_dashboard.html')

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
    aprendices = T_apre.objects.select_related('perfil__user').all()
    return render(request, 'aprendiz.html', {
        'aprendices': aprendices
    })


login_required


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


login_required


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
                new_perfil.rol = 'Lider'
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
login_required


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
        centroFormacion.delete()
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
            lector = csv.DictReader(datos_csv)
            
            for fila in lector:
                if 'username' not in fila:
                    print(f"Error: La columna 'username' está ausente en una fila: {fila}")
                    continue  # Salta esta fila y pasa a la siguiente

                # Generar contraseña aleatoria
                contraseña = generar_contraseña()

                # Crear el usuario
                user = User.objects.create_user(
                    username=fila['username'],
                    password=contraseña,
                    email=fila['email']
                )
                
                # Crear el perfil
                perfil = T_perfil.objects.create(
                    user=user,
                    nom=fila['nom'],
                    apelli=fila['apelli'],
                    tipo_dni=fila['tipo_dni'],
                    dni=fila['dni'],
                    tele=fila['tele'],
                    dire=fila['dire'],
                    gene=fila['gene'],
                    mail=fila['mail'],
                    fecha_naci=fila['fecha_naci'],
                    rol = "aprendiz"
                )

                repre = T_repre_legal.objects.create(
                    nom = fila['nom_repre'],
                    tele = fila['tele_repre'],
                    dire = fila['dire_repre'],
                    mail = fila['mail_repre'],
                    paren = fila['parentezco']
                )

                aprendiz = T_apre.objects.create(
                    cod = "z",
                    esta= "Activo",
                    perfil = perfil,
                    repre_legal = repre
                )

                 # Enviar el correo con la contraseña al usuario
                asunto = "Bienvenido a la plataforma"
                mensaje = f"Hola {fila['nom']} {fila['apelli']},\n\nTu cuenta ha sido creada con éxito. A continuación se encuentran tus credenciales:\n\nUsuario: {fila['username']}\nContraseña: {contraseña}\n\nRecuerda cambiar tu contraseña después de iniciar sesión."
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [fila['email']],
                    fail_silently=False,
                )

            return HttpResponseRedirect(reverse('aprendices'))
    else:
        form = CargarAprendicesMasivoForm()

    return render(request, 'aprendiz_masivo_crear.html', {'form': form})