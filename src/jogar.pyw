import pygame
from pygame.locals import *

from xadrez import Xadrez
from menu import Menu


size = (800, 800)
framerate = 60

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    janela = Xadrez()
    janela.carregar()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit(0)
            else:
                janela.event(event)

        if janela.draw(screen):
            pygame.display.flip()  # Atualiza toda tela (para atualizar função tem o update)

        nova_janela = janela.new()
        if nova_janela:
            janela = nova_janela

        clock.tick(framerate)
