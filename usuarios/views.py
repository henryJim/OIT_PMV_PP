from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import T_instructor, T_aprendiz, T_admin, T_lider
from .forms import InstructorForm, UserForm, PerfilForm
from django.db import IntegrityError

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else: 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': "El usuario o la contraseña es incorrecto"
            })    
        else:
            login(request, user)
            return redirect('home')

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
    instructores = T_instructor.objects.select_related('perfil').all()
    return render(request, 'instructor.html',{
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
                #Creacion del usuario
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()

                #creacion del perfil
                new_perfil = perfil_form.save(commit=False)
                new_perfil.user = new_user
                new_perfil.rol  = 'instructor'
                new_perfil.mail = new_user.email
                new_perfil.save()

                #creacion del instructor
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
    instructor = get_object_or_404(T_instructor, pk=instructor_id)
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
                return redirect('instructores')  # Redirigir a la lista de instructores (ajusta según sea necesario)
        except ValueError:
            # Si ocurre un error al guardar, mostrar el formulario nuevamente con el mensaje de error
            return render(request, 'instructor_detalle.html', {
                'instructor': instructor,
                'user_form': user_form,
                'perfil_form': perfil_form,
                'instructor_form': instructor_form,
                'error': "Error al actualizar el instructor. Verifique los datos."})

@login_required
def aprendices(request):
    aprendices = T_aprendiz.objects.select_related('perfil__user').all()
    return render(request, 'aprendiz.html',{
        'aprendices': aprendices
    })

@login_required
def novedades(request):
    return render(request, 'novedades.html')
