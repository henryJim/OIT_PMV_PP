from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from commons.models import T_instru, T_apre, T_admin, T_lider, T_nove
from .forms import InstructorForm, UserForm, PerfilForm, NovedadForm, AdministradoresForm
from django.db import IntegrityError
from django.http import JsonResponse
from django.forms.models import model_to_dict

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "El usuario o la contraseña es incorrecto"
            })
        else:
            login(request, user)
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


@login_required
def instructores(request):
    instructores = T_instru.objects.select_related('perfil').all()
    return render(request, 'instructor.html', {
        'instructores': instructores
    })


@login_required
def crear_instructor(request):

    if request.method == 'GET':

        user_form = UserForm()
        perfil_form = PerfilForm()
        instructor_form = InstructorForm()

        return render(request, 'instructor_crear.html', {
            'user_form': user_form,
            'perfil_form': perfil_form,
            'instructor_form': instructor_form
        })
    else:
        try:
            user_form = UserForm(request.POST)
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
        user_form = UserForm(instance=user)
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
            user_form = UserForm(request.POST, instance=user)
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


@login_required
def aprendices(request):
    aprendices = T_apre.objects.select_related('perfil__user').all()
    return render(request, 'aprendiz.html', {
        'aprendices': aprendices
    })


@login_required
def administradores(request):
    administradores = T_admin.objects.select_related('perfil__user').all()
    return render(request, 'administradores.html', {
        'administradores': administradores
    })


@login_required
def lideres(request):
    lideres = T_lider.objects.select_related('perfil__user').all()
    return render(request, 'lideres.html', {
        'lideres': lideres
    })


# Validar logica


@login_required
def crear_administradores(request):

    if request.method == 'GET':
        user_form = UserForm()
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
            user_form = UserForm(request.POST)
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
                # Redirigir a la lista de instructores (ajusta según sea necesario)
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
