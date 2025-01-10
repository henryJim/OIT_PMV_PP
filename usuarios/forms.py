from django import forms
from django.contrib.auth.models import User
from commons.models import T_instru, T_perfil, T_nove, T_admin, T_apre, T_lider, T_repre_legal, T_munici, T_departa, T_insti_edu, T_centro_forma


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
        exclude = ['perfil', 'ficha']
        widgets = {
            'cod': forms.TextInput(attrs={'class': 'form-control'}),
            'esta': forms.Select(attrs={'class': 'form-control'}),
            'repre_legal': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'cod': 'Codigo',
            'esta':  'Estado',
            'repre_legal':  'Represante Legal'
        }


class RepresanteLegalForm(forms.ModelForm):
    class Meta:
        model = T_repre_legal
        fields = ['nom', 'tele', 'dire', 'mail', 'paren', 'ciu', 'depa']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'tele': forms.TextInput(attrs={'class': 'form-control'}),
            'dire': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.TextInput(attrs={'class': 'form-control'}),
            'paren': forms.TextInput(attrs={'class': 'form-control'}),
            'ciu': forms.TextInput(attrs={'class': 'form-control'}),
            'depa': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'nom': 'Nombre',
            'tele': 'Telefono',
            'dire': 'Direccion',
            'mail': 'Correo',
            'paren': 'Parentesco',
            'ciu': 'Ciudad',
            'depa': 'Departamento'
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


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = T_departa
        fields = ['cod_departa', 'nom_departa']
        widgets = {
            'cod_departa': forms.TextInput(attrs={'class': 'form-control'}),
            'nom_departa': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cod_departa': 'Codigo de departamento',
            'nom_departa': 'Departamento',
        }


class MunicipioForm(forms.ModelForm):
    class Meta:
        model = T_munici
        fields = ['cod_munici', 'nom_munici', 'nom_departa']
        widgets = {
            'cod_munici': forms.TextInput(attrs={'class': 'form-control'}),
            'nom_munici': forms.TextInput(attrs={'class': 'form-control'}),
            'nom_departa': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cod_munici': 'Codigo de municipio',
            'nom_munici': 'Municipio',
            'nom_departa': 'Departamento',
        }


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = T_insti_edu
        fields = ['nom', 'dire', 'secto', 'pote_apre', 'depa', 'muni', 'coordi', 'coordi_mail', 'coordi_tele', 'esta', 'insti_mail', 'recto', 'recto_tel']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'dire': forms.TextInput(attrs={'class': 'form-control'}),
            'secto': forms.Select(attrs={'class': 'form-control'}),
            'pote_apre': forms.TextInput(attrs={'class': 'form-control'}),
            'depa': forms.Select(attrs={'class': 'form-control'}),
            'muni': forms.Select(attrs={'class': 'form-control'}),
            'coordi': forms.TextInput(attrs={'class': 'form-control'}),
            'coordi_mail': forms.TextInput(attrs={'class': 'form-control'}),
            'coordi_tele': forms.TextInput(attrs={'class': 'form-control'}),
            'esta': forms.Select(attrs={'class': 'form-control'}),
            'insti_mail': forms.TextInput(attrs={'class': 'form-control'}),
            'recto': forms.TextInput(attrs={'class': 'form-control'}),
            'recto_tel': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nom': 'Nombre institución',
            'dire': 'Dirección institución',
            'secto': 'Sector',
            'pote_apre': 'Aprendices potenciales',
            'depa': 'Departamento',
            'muni': 'municipio',
            'coordi': 'Coordinador',
            'coordi_mail': 'Correo coordinador',
            'coordi_tele': 'Telefono coordinador',
            'esta': 'Estado',
            'insti_mail': 'Correo institucion',
            'recto': 'Nombre Rector',
            'recto_tel': 'Telefono rector'
        }


class CentroFormacionForm(forms.ModelForm):
    class Meta:
        model = T_centro_forma
        fields = ['nom', 'dire', 'depa', 'muni']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'dire': forms.TextInput(attrs={'class': 'form-control'}),
            'depa': forms.TextInput(attrs={'class': 'form-control'}),
            'muni': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nom': 'Nombre de centro de formacion',
            'dire': 'Dirección del centro de formación',
            'depa': 'Departamento del centro de formación',
            'muni': 'Municipio del centro de formación',
        }

class CargarAprendicesMasivoForm(forms.Form):
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Seleccione un archivo CSV"
    )