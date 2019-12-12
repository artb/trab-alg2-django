
from django import forms
from .models import Resultado


class TrabalhoAlgebraForm(forms.Form):
    matriz = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'[\n[a1,a2,a3],\n[b1,b2,b3],\n[c1,c2,c3]\n]'}))
    determinante = forms.BooleanField(required=False)
    traco = forms.BooleanField(required=False)
    transposta = forms.BooleanField(required=False)
    inversa = forms.BooleanField(required=False)
    polinomio_caracteristico = forms.BooleanField(required=False)
    autovalores = forms.BooleanField(required=False)
    autovetores = forms.BooleanField(required=False)
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
            'autovetores',
            'matriz_diagonal'
        ]