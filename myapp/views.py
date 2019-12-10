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
            matriz_diagonal = form.cleaned_data['matriz_diagonal']
            t = Resultado(id=1, matriz=matriz, determinante=determinante, traco=traco, transposta=transposta,
                          inversa=inversa, polinomio_caracteristico=polinomio_caracteristico, autovalores=autovalores,
                          matriz_diagonal=matriz_diagonal)
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
    matriz = numpy.array(matriz, dtype=float)
    macaco = numpy.array(matriz, dtype=float)
    print(matriz)
    request.matriz = str(matriz)

    if request.determinante:
        determinante = determinantOfMatrix(matriz)
        request.determinante = determinante

    if request.traco:
        request.traco = traco(macaco)

    if request.transposta:
        aux = array(macaco).T
        request.transposta = str(aux)

    if request.inversa:
        aux = numpy.linalg.inv(macaco)
        request.inversa = str(aux)

    if request.polinomio_caracteristico:
        request.polinomio_caracteristico = polinomioCaracteristico(macaco)

    if request.autovalores:
        request.autovalores = QR(macaco)

    if request.matriz_diagonal:
        aux = matrizDiagonal(macaco)
        request.matriz_diagonal = str(aux)

    return request


# XXXXXXXXXXXXXX APENAS FUNCOES MATERMATICAS PARA BAIXO XXXXXXXXXX
def determinantOfMatrix(mat):
    n = len(mat)
    temp = [0] * n
    total = 1
    det = 1

    # loop iterando pelos elementos em diagonal
    for i in range(0, n):
        index = i

        # Pega os valores da coluna exterior procurando por uma que o valor nao é zero
        while (mat[index][i] == 0 and index < n):
            index += 1

        if (index == n):  # se nao encontramos nenhum valor diferente de zero
            # interrompe esse laço e recomeça um novo laço la no for
            continue

        if (index != i):
            # troco de lugar o index e o valor da linha
            for j in range(0, n):
                mat[index][j], mat[i][j] = mat[i][j], mat[index][j]

                # troca o sinal do determinante ao trocar de linha
            det = det * int(pow(-1, index - i))

            # guardando os valores da diagonal
        for j in range(0, n):
            temp[j] = mat[i][j]

            # fazendo a transversal dos valores embaixo da matriz principal
        for j in range(i + 1, n):
            num1 = temp[i]  # valor da matriz principal
            num2 = mat[j][i]  # valor da linha nao principal

            # fazendo a transversal das outras linhas
            # e multiplicando as linhas
            for k in range(0, n):
                mat[j][k] = (num1 * mat[j][k]) - (num2 * temp[k])

            total = total * num1  # Det(kA)=kDet(A);

    # multiplicando a transversal para pegar o determinante
    for i in range(0, n):
        det = det * mat[i][i]

    return int(det / total)  # Det(kA)/k=Det(A);

def traco(p_matriz):
    print(p_matriz)
    traco = 0
    n = len(p_matriz)
    for i in range(n):
        for j in range(n):
            if (i == j):
                print(p_matriz[i][j])
                traco += p_matriz[i][j]
    return traco


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