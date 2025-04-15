from django import forms
from django.contrib.auth.models import User
from commons.models import T_acti,T_guia, T_centro_forma,T_fase_ficha, T_docu,T_departa, T_insti_edu, T_munici, T_DocumentFolder, T_encu,T_apre, T_raps_ficha, T_acti_docu, T_acti_ficha, T_acti_apre, T_acti_descri, T_crono, T_progra, T_compe, T_raps, T_ficha
from django.db.models import Subquery



class FichaForm(forms.ModelForm):
    class Meta:
        model = T_ficha
        fields = [ 'num_apre_proce', 'progra']
        widgets = {
            'num_apre_proce': forms.TextInput(attrs={'class': 'form-control'}), 
            'progra': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'num_apre_proce': 'Numero de aprendices en proceso', 
            'progra': 'Programa de formacion'
        }

class CascadaMunicipioInstitucionForm(forms.Form):
    departamento = forms.ModelChoiceField(
        queryset=T_departa.objects.all(),
        required=False,
        empty_label="Selecciona un departamento",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_departamento'})
    )
    municipio = forms.ModelChoiceField(
        queryset=T_munici.objects.none(),  # Inicialmente vacío
        required=False,
        empty_label="Selecciona un municipio",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_municipio'})
    )
    centro = forms.ModelChoiceField(
        queryset=T_centro_forma.objects.none(),
        required=False,
        empty_label="Selecciona un centro",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_centro'})
    )
    insti = forms.ModelChoiceField(
        queryset=T_insti_edu.objects.none(),  # Inicialmente vacío
        required=False,
        empty_label="Selecciona una institución",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_insti'})
    )


class ActividadForm(forms.ModelForm):
    class Meta:
        model = T_acti
        fields = ['nom', 'descri', 'tipo', 'guia']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la actividad'}),
            'descri': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la actividad'}),
            'tipo': forms.SelectMultiple(attrs={'class': 'form-select tomselect-multiple', 'placeholder': 'Seleccione los tipos de actividad'}),
            'guia': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'nom': 'Nombre',
            'descri': 'Descripcion',
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
            'archi': 'Archivo'
        }

class RapsFichaForm(forms.Form):
    raps = forms.ModelMultipleChoiceField(
        queryset=T_raps_ficha.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select tomselect-raps',
            'placeholder': 'Seleccione los RAPs asociados'
        }),
        required=True
    )

    def __init__(self, *args, **kwargs):
        ficha = kwargs.pop('ficha', None)
        super().__init__(*args, **kwargs)

        if ficha:
            fase_activa = T_fase_ficha.objects.filter(
                ficha=ficha,
                vige='1'
            ).first()

            if fase_activa:
                fase_nom = fase_activa.fase
                self.fields['raps'].queryset = T_raps_ficha.objects.filter(
                    ficha=ficha,
                    rap__compe__fase=fase_nom
                )

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
        }
        labels = {
            'nom': 'Nombre',
            'compe': 'Competencia',
        }

class GuiaForm(forms.ModelForm):
    class Meta:
        model = T_guia
        fields = ['nom', 'horas_auto', 'horas_dire', 'progra']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'label': 'Ingrese el nombre'}),
            'horas_auto': forms.TextInput(attrs={'class': 'form-control'}),
            'horas_dire': forms.TextInput(attrs={'class': 'form-control'}),
            'progra': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nom': 'Nombre',
            'horas_auto': 'Horas autonomas',
            'horas_dire': 'Horas directas',
            'progra': 'Programa',
        }

class EncuentroForm(forms.ModelForm):
    class Meta:
        model = T_encu
        fields = ['tema', 'lugar']
        widgets = {
            'tema': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tema': 'Tema del encuentro',
            'lugar': 'Lugar de encuentro'
        }

class EncuApreForm(forms.Form):
    aprendices = forms.ModelMultipleChoiceField(
        queryset=T_apre.objects.none(),  # Inicialmente vacío
        widget=forms.CheckboxSelectMultiple,  # Widget de checkboxes
        required=False  # No es obligatorio seleccionar RAPs
    )

    def __init__(self, *args, **kwargs):
        ficha = kwargs.pop('ficha', None)  # Extraer 'ficha' de los argumentos
        super().__init__(*args, **kwargs)  # Llamar al constructor de la clase base
        if ficha:
            # Si se pasó una ficha, ajustar el queryset para incluir los RAPs de la ficha
            self.fields['aprendices'].queryset = T_apre.objects.filter(ficha=ficha)

class CargarDocuPortafolioFichaForm(forms.Form):
    nombre_documento = forms.CharField(max_length=255, label="Nombre del Documento")
    url_documento = forms.URLField(label="URL del Documento")
