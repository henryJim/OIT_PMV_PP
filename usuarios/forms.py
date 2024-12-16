from django import forms
from django.contrib.auth.models import User
from .models import T_instructor, T_perfil


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba la contraseña'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el mail'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Contraseña',
            'email': 'Correo electrónico',
        }
        help_texts = {
            'password': None,
            'username': None
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = T_perfil
        exclude = ['user', 'rol', 'mail']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apelli': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'tipo_dni': forms.Select(attrs={'class': 'form-select'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'tele': forms.NumberInput(attrs={'class': 'form-control'}),
            'dire': forms.TextInput(attrs={'class': 'form-control'}),
            'gene': forms.Select(attrs={'class': 'form-select'}),
            'fecha_naci': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'nombre': 'Nombres',
            'apelli': 'Apellidos',
            'tipo_dni': 'Tipo de documento',
            'dni': 'Numero de documento',
            'tele': 'Telefono',
            'dire': 'Direccion',
            'gene': 'Genero',
            'fecha_naci': 'Fecha de nacimiento'
        }

class InstructorForm(forms.ModelForm):
    class Meta:
        model = T_instructor
        exclude = ['perfil']  # El perfil se asignará automáticamente
        widgets = {
            'contra': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ini': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'esta': forms.TextInput(attrs={'class': 'form-control'}),
            'profe': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_vincu': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'contra': 'Numero de contrato',
            'fecha_ini': 'Fecha de inicio',
            'fecha_fin': 'Fecha de finalizacion',
            'esta': 'Estado',
            'profe': 'Profesion',
            'tipo_vincu': 'Tipo de vinculacion'
        }
