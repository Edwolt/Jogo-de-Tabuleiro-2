import pygame
from pygame import display
from pygame.time import Clock
from pygame.locals import *

from xadrez import iniciar_xadrez
from menu import Menu
from loading import Loading
from recursos import Recursos


if __name__ == '__main__':
    pygame.init()
    recursos = Recursos('bordas', size=(800, 800), framerate=60)

    screen = display.set_mode(recursos.size)
    clock = Clock()

    janela = iniciar_xadrez(recursos)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit(0)
            else:
                janela.event(event)

        janela.draw(screen)
        janela = janela.new()

        if not isinstance(janela, Loading):
            clock.tick(recursos.framerate)
