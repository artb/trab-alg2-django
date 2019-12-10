
from django import forms
from .models import Resultado


class TrabalhoAlgebraForm(forms.Form):
    matriz = forms.CharField(widget=forms.Textarea)
    determinante = forms.BooleanField(required=False)
    traco = forms.BooleanField(required=False)
    transposta = forms.BooleanField(required=False)
    inversa = forms.BooleanField(required=False)
    polinomio_caracteristico = forms.BooleanField(required=False)
    autovalores = forms.BooleanField(required=False)
    matriz_diagonal = forms.BooleanField(required=False)


class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        fields = [
            'matriz',
            'determinante',
            'traco',
            'transposta',
            'inversa',
            'polinomio_caracteristico',
            'autovalores',
            'matriz_diagonal'
        ]