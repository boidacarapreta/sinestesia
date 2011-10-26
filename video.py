# -*- coding: utf-8 -*-


import os
import pygame
from pygame.locals import *

import audio
	

class mouseSprite(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((1, 1))
		self.rect = self.image.get_rect()


class retanguloSprite(pygame.sprite.Sprite):
	def __init__(self, posicao, tamanho, cor):
		pygame.sprite.Sprite.__init__(self)
		# Imagem
		self.image = pygame.Surface(tamanho)
		self.cor = cor
		self.image.fill(CorHTMLparaRGB(self.cor))
		# Retângulo
		self.rect = self.image.get_rect()
		self.rect.topleft = posicao
		

# Literalmente copiado de: http://code.activestate.com/recipes/266466/
def RGBparaCorHTML(tupla_rgb):
	hexcolor = '#%02x%02x%02x' % tupla_rgb
	return hexcolor


# Idem a anterior
def CorHTMLparaRGB(cor):
	cor = cor.strip()
	if cor[0] == '#': cor = cor[1:]
	if len(cor) != 6:
		raise ValueError, "#%s não está em formato de cor HTML: #RRGGBB" % cor
	r, g, b = cor[:2], cor[2:4], cor[4:]
	r, g, b = [int(n, 16) for n in (r, g, b)]
	return (r, g, b)


def importarRetangulos(diretorio, retangulos):
	arquivos = os.listdir(diretorio)
	for arquivo in arquivos:
		if (os.path.isfile(os.path.join(diretorio, arquivo))):
			conf = open(os.path.join(diretorio,arquivo), 'r')
			for linha in conf:
				tokens = linha.strip().split(',')
				if tokens[0] == 'rect':
					try:
						retangulo = retanguloSprite((int(tokens[1]), int(tokens[2])),
							(int(tokens[3]), int(tokens[4])), tokens[5])
						retangulos.add(retangulo)
					except:
						print('Erro ao importar a figura: ' + linha.strip())
	return retangulos