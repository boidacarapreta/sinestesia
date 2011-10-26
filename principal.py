#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
try:
	import pygame
	from pygame.locals import *
except:
	print("Pygame não instalado! Como assim?!?!")
	sys.exit()

import audio
import video
import rede
import xmpp


def main():
	# Tela
	# pygame.mixer.pre_init(44100, -16, 2, 4096)
	pygame.sndarray.use_arraytype("numpy")
	pygame.init()
	janela = pygame.display.set_mode((0, 0), DOUBLEBUF | HWSURFACE | FULLSCREEN, 32)
	pygame.display.set_caption("IP")
	superficie = pygame.Surface(janela.get_size()).convert()
		
	# Sprites
	diretorio = 'figuras'
	mouse = video.mouseSprite()
	retangulos = pygame.sprite.LayeredUpdates()
	video.importarRetangulos(diretorio, retangulos)
	retangulos.draw(superficie)

	# Frequências: criando dicionário de cor:som
	diretorio = 'sons'
	sons = audio.importaFrequencias(diretorio)

	# Conectar no XMPP
	diretorio = 'conf'
	xmpp.init(diretorio)

	# Relógio
	relogio = pygame.time.Clock()

	# "Corpo" do programa
	tocando = []
	running = True
	while running:
		# Limpa a tela. Deixa apenas o fundo intacto:
		retangulos.clear(janela, superficie)
		janela.blit(superficie, (0, 0))

		# Intercepta e atende a uma fila de eventos:
		for evento in pygame.event.get():
			if evento.type == QUIT or (evento.type == KEYDOWN and evento.key in [K_ESCAPE, K_q]):
				running = False
			elif evento.type == KEYDOWN and evento.key in [K_f]:
				janela = pygame.display.set_mode((800, 600), 0, 32)

			# Atualiza os trechos de tela onde há novidade: os retângulos
			retangulos.draw(superficie)

			# Localiza na superfície o mouse e procura pelas colisões com retângulo
			mouse.rect.topleft = pygame.mouse.get_pos()
			mouseSobre = pygame.sprite.spritecollide(mouse, retangulos, False)

			# Compara se o mouse "entrou" em um retângulo: toca!
			for retangulo in mouseSobre:
				try:
					indice = tocando.index(retangulo)
				except:
					if sons.has_key(retangulo.cor):
						canal = sons[retangulo.cor].onda.play(-1)
						# Toca a frequência (estéreo se possível):
						if sons[retangulo.cor].onda.get_num_channels() == 2:
							esquerdo, direito = audio.estereo(retangulo.rect.topleft[0],
								janela.get_size()[0])
							canal.set_volume(esquerdo, direito)
						tocando.append(retangulo)
			
			# Lista os retângulos de onde o mouse "saiu": para de tocar!
			for retangulo in tocando:
				try:
					mouseSobre.index(retangulo)
				except:
					# Não está mais tocando
					canal = sons[retangulo.cor].onda.stop()
					tocando.remove(retangulo)

		# É uma solução ruim: parte do laço fica dentro do "for evento..."
		# e parte fica fora: independe se há ou não eventos (mouse parado, por exemplo)
		# Se ficasse dentro do laço, o texto só apareceria com o mouse em contínuo movimento :-/
		for retangulo in tocando:
			# Continua tocando: adiciona o texto próximo ao mouse
			figura = sons[retangulo.cor]
			figura.textoPos.centerx = mouse.rect.centerx
			figura.textoPos.centery = mouse.rect.centery - 20
			janela.blit(figura.texto, figura.textoPos)

		# Atualiza a tela e mantém por 1/30s -> 30fps
		pygame.display.flip()
		relogio.tick(30)


# Principal
if __name__ == '__main__':
	main()
