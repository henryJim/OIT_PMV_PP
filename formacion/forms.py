from django import forms
from django.contrib.auth.models import User
from commons.models import T_acti, T_docu, T_acti_docu, T_acti_ficha, T_acti_apre, T_acti_descri, T_crono, T_progra, T_compe, T_raps, T_admin


class ActividadForm(forms.ModelForm):
    class Meta:
        model = T_acti
        fields = ['nom', 'descri', 'horas_auto', 'horas_dire', 'tipo', 'guia']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre'}),
            'descri': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba la descripcion de la actividad'}),
            'horas_auto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba las horas autonomas'}),
            'horas_dire': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba las horas directas'}),
            'tipo': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'guia': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'nom': 'Nombre',
            'descri': 'Descripcion',
            'horas_auto': 'Horas autonomas',
            'horas_dire': 'Horas directas',
            'tipo': 'Tipo de actividad',
            'guia': 'Guia relacionada'
        }


class DocumentosForm(forms.ModelForm):
    class Meta:
        model = T_docu
        exclude = ['nom', 'tipo', 'tama', 'priva', 'esta']
        widgets = {
            'archi': forms.FileInput(attrs={'class': 'form-select'})
        }
        labels = {
            'archi': 'Archivos'
        }


class CronogramaForm(forms.ModelForm):
    class Meta:
        model = T_crono
        fields = ['nove', 'fecha_ini_acti', 'fecha_fin_acti',
                  'fecha_ini_cali', 'fecha_fin_cali']
        widgets = {
            'nove': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba las novedades si aplican'}),
            'fecha_ini_acti': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin_acti': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_ini_cali': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin_cali': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        labels = {
            'nove': 'Novedades',
            'fecha_ini_acti': 'Fecha de inicio actividad',
            'fecha_fin_acti': 'Fecha finalizacion actividad',
            'fecha_ini_cali': 'Fecha de inicio calificacion',
            'fecha_fin_cali': 'Fecha finalizacion calificacion'
        }


class ProgramaForm(forms.ModelForm):
    class Meta:
        model = T_progra
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'label': 'Ingrese el nombre del programa'})
        }
        labels = {
            'nom': 'Nombre del programa'
        }


class CompetenciaForm(forms.ModelForm):
    class Meta:
        model = T_compe
        fields = ['nom', 'progra', 'fase']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'label': 'Ingrese el nombre de la competencia'}),
            'progra': forms.Select(attrs={'class': 'form-control'}),
            'fase': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'nom': 'Nombre',
            'progra': 'Programa',
            'fase': 'Fase'
        }


class RapsForm(forms.ModelForm):
    class Meta:
        model = T_raps
        exclude = ['comple']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'label': 'Ingrese el nombre'}),
            'compe': forms.Select(attrs={'class': 'form-control'}),
            'fase': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'nom': 'Nombre',
            'compe': 'Competencia',
            'fase': 'Fase'
        }
