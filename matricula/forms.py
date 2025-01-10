from django import forms
from commons.models import T_apre

class AsignarAprendicesFichaForm(forms.Form):
    aprendices = forms.ModelMultipleChoiceField(
        queryset=T_apre.objects.filter(ficha__isnull=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )