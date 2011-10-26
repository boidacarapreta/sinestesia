# -*- coding: utf-8 -*-


import os
try:
	import numpy
except:
	print("Numpy não instalado! Como assim?!?!")
	sys.exit()
import pygame


class som:
	def __init__(self, frequencia):
		self.frequencia = frequencia
		self.onda = tom(frequencia)
		self.fonte = pygame.font.Font(pygame.font.get_default_font(), 20)
		self.texto = self.fonte.render(truncar(self.frequencia, 2), 1, (255,255,255))
		self.textoPos = self.texto.get_rect()


# Funções
def truncar(numero, digitos):
	parte = str(numero).split('.')
	return parte[0] + '.' + parte[1][0:digitos]

	
def tom(frequencia):
	# 8000 amostras em cosseno, convertidas (-1,1) -> (-32767,32767) e duplicado
	# o vetor (estéreo)
	amostras = numpy.arange(-1, 1, 1.0 / 8000, dtype=numpy.float)
	vetorSimples = numpy.cos(2 * numpy.pi * frequencia * amostras)
	vetorSimples *= 2**15-1
	vetorSimples = vetorSimples.astype("int16")
	vetorDuplo = numpy.repeat(vetorSimples, 2)
	vetorDuplo.resize(16000, 2)
	return pygame.sndarray.make_sound(vetorDuplo)


def estereo(x, eixoX):
	direito = float(x) / eixoX
	esquerdo = 1.0 - direito
	return(esquerdo, direito)


def importaFrequencias(diretorio):
	sons = {}
	arquivos = os.listdir(diretorio)
	for arquivo in arquivos:
		if (os.path.isfile(os.path.join(diretorio, arquivo))):
			conf = open(os.path.join(diretorio,arquivo), 'r')
			for linha in conf:
				tokens = linha.strip().split(',')
				try:
					umSom = som(float(tokens[1]))
					sons.update({tokens[0]:umSom})
				except:
					print('Erro ao importar o som: ' + linha.strip())
	return sons
