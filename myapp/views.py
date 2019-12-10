from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import TrabalhoAlgebraForm, ResultadoForm
from .models import Resultado
import numpy
from numpy import *


# Create your views here.
def sobre(request):
    return render(request, 'sobre.html')

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
            t = Resultado(id=1, matriz=matriz, determinante=determinante, traco=traco, transposta=transposta,
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
        aux = numpy.linalg.inv(matriz)
        request.inversa = str(aux)

    if request.polinomio_caracteristico:
        request.polinomio_caracteristico = polinomioCaracteristico(matriz)

    if request.autovalores:
        request.autovalores = QR(matriz)

    if request.matriz_diagonal:
        request.matriz_diagonal = matrizDiagonal(matriz)

    return request


# XXXXXXXXXXXXXX APENAS FUNCOES MATERMATICAS PARA BAIXO XXXXXXXXXX

def traco(matrix):
    n = len(matrix)
    assert n == len(matrix[0])
    return sum(matrix[i][i] for i in range(n))


def matrizTransposta(matriz):
    tam = len(matriz)
    matrizTransposta = []  # lista vazia para receber a transposta
    linha = []  # lista auxiliar para receber as linhas
    for i in range(tam):
        for j in range(tam):
            linha.append(matriz[j][i])  # recebe a coluna como linha
        matrizTransposta.append(linha)  # recebe a linha
        linha = []  # reseta o auxiliar
        return matrizTransposta


def somaCoeficientes(matriz, n, q):
    for i in range(n):
        matriz[i][i] += q


def polinomioCaracteristico(matriz):
    A = array(matriz)
    n = len(A)
    c = [1.0]
    B = array(A)
    for i in range(1, n + 1):
        c.append(-traco(B) / i)
        somaCoeficientes(B, n, c[i])
        B = dot(A, B)
    return c


def verificaMatrizTriangular(A):
    for i in range(1, len(A)):
        for j in range(i):
            if abs(A[i][j]) > 0.0001:
                return 1
    return 0


def zeraElementos(A, i, j):
    U = identity(len(A))
    U[i][i] = A[0][0] / (((A[0][0] ** 2) + A[i][j] ** 2) ** 0.5)
    U[j][j] = U[i][i]
    U[j][i] = A[i][j] / (((A[0][0] ** 2) + A[i][j] ** 2) ** 0.5)
    U[i][j] = -U[j][i]
    return U


def QR(A):
    cont = 0
    tam = len(A)
    av = []
    while verificaMatrizTriangular(A) and cont < 1000:
        Q = identity(tam)
        for i in range(1, tam):
            for j in range(i):
                if A[i][j] != 0:
                    U = zeraElementos(A, i, j)
                    Q = dot(U, Q)
                    A = dot(U, A)

        Q = Q.T
        A = dot(A, Q)
        cont += 1
    for i in range(tam):
        av.append(A[i][i])
    return av

def matrizDiagonal(A):
	n = len(A)
	matriz = zeros((n,n))
	autovalores = linalg.eig(A)[0]
	for i in range(n):
		matriz[i][i] = autovalores[i]
	return matriz