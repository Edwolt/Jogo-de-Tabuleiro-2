import pygame
from pygame import display
from pygame.time import Clock
from pygame.locals import *

from xadrez import iniciar_xadrez
from menu import Menu


size = (800, 800)
framerate = 60

if __name__ == '__main__':
    pygame.init()
    screen = display.set_mode(size)
    clock = Clock()

    janela = iniciar_xadrez()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit(0)
            else:
                janela.event(event)

        janela.draw(screen)
        janela = janela.new()

        clock.tick(framerate)
