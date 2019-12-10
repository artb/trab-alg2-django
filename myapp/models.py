from django.db import models

class Resultado(models.Model):
        matriz = models.CharField(max_length=320)
        determinante = models.BooleanField()
        traco = models.BooleanField()
        transposta = models.BooleanField()
        inversa = models.BooleanField()
        polinomio_caracteristico = models.BooleanField()
        autovalores = models.BooleanField()
        autovetores = models.BooleanField()
        matriz_diagonal = models.BooleanField()

