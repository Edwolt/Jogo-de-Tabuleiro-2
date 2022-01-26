from __future__ import annotations

import pygame as pg

from recursos import Recursos
from janelas import Loading, Xadrez


# TODO separar pastas de fonte e imagens em assets
def main():
    pg.init()
    recursos = Recursos(size=(800, 800), framerate=60, min_png=True)
    recursos.set_config("bordas")

    screen = pg.display.set_mode(recursos.size)
    clock = pg.time.Clock()

    janela = Loading(recursos.carregar(), Xadrez())

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit(0)
            else:
                janela.event(event)

        janela.draw(screen)
        janela = janela.new()

        if not isinstance(janela, Loading):
            clock.tick(recursos.framerate)


if __name__ == "__main__":
    main()
