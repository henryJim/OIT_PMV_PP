from django import forms
from django.contrib.auth.models import User
from commons.models import T_instru, T_perfil, T_nove, T_admin, T_apre, T_lider


class UserFormEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password']
        widgets = {

            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el mail'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        help_texts = {

            'username': None
        }


class UserFormCreate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre de usuario'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba la contraseña de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el mail'}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Contraseña',
            'email': 'Correo electrónico',
        }
        help_texts = {
            'username': None,
            'password': None
        }


class PerfilForm(forms.ModelForm):
    class Meta:
        model = T_perfil
        exclude = ['user', 'rol', 'mail']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apelli': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'tipo_dni': forms.Select(attrs={'class': 'form-select'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'tele': forms.NumberInput(attrs={'class': 'form-control'}),
            'dire': forms.TextInput(attrs={'class': 'form-control'}),
            'gene': forms.Select(attrs={'class': 'form-select'}),
            'fecha_naci': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'nom': 'Nombres',
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
        model = T_instru
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


class AprendizForm(forms.ModelForm):
    class Meta:
        model = T_apre
        exclude = ['perfil']
        widgets = {
            'cod': forms.TextInput(attrs={'class': 'form-control'}),
            'esta': forms.Select(attrs={'class': 'form-control'}),
            'ficha': forms.Select(attrs={'class': 'form-select'}),
            'repre_legal': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'cod': 'Codigo',
            'esta':  'Estado',
            'ficha':  'ficha',
            'repre_legal':  'Represante Legal'
        }


class NovedadForm(forms.ModelForm):
    class Meta:
        model = T_nove
        exclude = ['estado']  # El estado se asignara automaticamente
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descri': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'sub_tipo': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'nombre': 'Nombre',
            'descri': 'Descripcion',
            'tipo': 'Tipo',
            'sub_tipo': 'Sub Tipo'
        }


class AdministradoresForm(forms.ModelForm):
    class Meta:
        model = T_admin
        exclude = ['perfil']
        field = ['area', 'esta']
        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'esta': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'area': 'Area',
            'esta':  'Estado'
        }


class LiderForm(forms.ModelForm):
    class Meta:
        model = T_lider
        exclude = ['perfil']
        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'esta': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'area': 'Area',
            'esta':  'Estado'
        }
