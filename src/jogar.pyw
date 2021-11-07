from __future__ import annotations

import pygame
from pygame import display
from pygame.time import Clock
from pygame.locals import QUIT

from recursos import Recursos
from janelas import Loading, Xadrez


def main():
    pygame.init()
    recursos = Recursos(size=(800, 800), framerate=60, png_min=True)
    recursos.set_config('bordas')

    screen = display.set_mode(recursos.size)
    clock = Clock()

    janela = Loading(recursos.carregar(), Xadrez())

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


if __name__ == '__main__':
    main()
