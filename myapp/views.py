from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from.forms import TrabalhoAlgebraForm, ResultadoForm
from .models import Resultado
import numpy
from numpy import *
from numpy.linalg import inv

# Create your views here.
def homepage(request):
    form = TrabalhoAlgebraForm()
    return render(request, 'form.html', {'form': form})

def create(request):
    print(request)
    if request.method == "POST":
        form = TrabalhoAlgebraForm(request.POST)
        if form.is_valid():
            matriz = form.cleaned_data['matriz']
            determinante = form.cleaned_data['determinante']
            traco = form.cleaned_data['traco']
            transposta = form.cleaned_data['transposta']
            inversa = form.cleaned_data['inversa']
            polinomio_caracteristico = form.cleaned_data['polinomio_caracteristico']
            autovalores = form.cleaned_data['autovalores']
            autovetores = form.cleaned_data['autovetores']
            matriz_diagonal = form.cleaned_data['matriz_diagonal']
            t = Resultado(id = 1, matriz=matriz, determinante=determinante, traco=traco, transposta=transposta,
                          inversa=inversa, polinomio_caracteristico=polinomio_caracteristico, autovalores=autovalores,
                          autovetores=autovetores, matriz_diagonal=matriz_diagonal)
            t.save()
            return HttpResponseRedirect("/resultado/")

        else:
            form = TrabalhoAlgebraForm()

    form = TrabalhoAlgebraForm()

    return render(request, 'form.html', {'form': form})

def resultado_detail(request):
    resultado = Resultado.objects.get(id=1)
    resultado = processa_request(resultado)
    context = {
        "object": resultado
    }
    return render(request, 'resultado.html', context)

def processa_request(request):
    matriz = eval(request.matriz)
    request.matriz = matriz

    if request.determinante:
        determinante = numpy.linalg.det(matriz)
        request.determinante = determinante

    if request.traco:
        request.traco = traco(matriz)

    if request.transposta:
        request.transposta = matrizTransposta(matriz)

    if request.inversa:
        request.inversa = inv(matriz)

    if request.polinomio_caracteristico:
        request.polinomio_caracteristico = polinomioCaracteristico(matriz)

    return request


# XXXXXXXXXXXXXX APENAS FUNCOES MATERMATICAS PARA BAIXO XXXXXXXXXX

def traco(matrix):
    n = len(matrix)
    assert n == len(matrix[0])
    return sum(matrix[i][i] for i in range(n))

def matrizTransposta(matriz):
	tam = len(matriz)
	matrizTransposta = [] # lista vazia para receber a transposta
	linha = [] # lista auxiliar para receber as linhas
	for i in range(tam):
		for j in range(tam):
			linha.append(matriz[j][i]) # recebe a coluna como linha
		matrizTransposta.append(linha) # recebe a linha
		linha = [] # reseta o auxiliar
		return matrizTransposta


def somaCoeficientes(matriz, n, q):
    for i in range(n):
        matriz[i][i] += q


def traco(matrix, n):
    sum = 0
    for i in range(n):
        sum += matrix[i][i]
    return sum


def polinomioCaracteristico(matriz):
    A = array(matriz)
    n = len(A)
    c = [1.0]
    B = array(A)
    for i in range(1, n + 1):
        c.append(-traco(B, n) / i)
        somaCoeficientes(B, n, c[i])
        B = dot(A, B)
    return c