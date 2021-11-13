from __future__ import annotations

import pygame as pg

import tipos as tp
from recursos import Recursos

from .abc_janela import Janela


class Loading(Janela):
    def __init__(self, carregamento: tp.load_gen, janela: Janela):
        self.janela = janela

        self.finalizado = False
        self.carregamento = carregamento

        recursos = Recursos()
        self.fonte = recursos.config.fonte(25)
        self.fonte_loading = recursos.config.fonte(50)

    ##### Interface #####
    def event(self, event: pg.event.Event) -> None:
        pass

    def draw(self, canvas: pg.Surface) -> None:
        recursos = Recursos()
        canvas.fill(pg.Color(0, 0, 0))

        try:
            barras = next(self.carregamento)
        except StopIteration:
            self.finalizado = True
            return

        x, y = 10, 10
        espaco = 10
        w = canvas.get_size()[0]
        barra_w, barra_h = w - 2 * x, 30

        texto = 'Loading'
        tam_x, tam_y = self.fonte_loading.size(texto)
        texto = self.fonte_loading.render(texto, False, pg.Color(255, 255, 255))
        meio = w/2 - tam_x/2
        canvas.blit(texto, (meio, y))

        y += tam_y + 2 * espaco

        for tam, val in barras:
            cor_carregado, cor_falta = recursos.config.loading_cores()
            pg.draw.rect(
                canvas,
                cor_falta,
                pg.Rect(x, y, barra_w, barra_h)
            )
            pg.draw.rect(
                canvas,
                cor_carregado,
                pg.Rect(x, y, barra_w * (val/tam), barra_h)
            )

            texto = f'{val} / {tam}'
            tam_x, tam_y = self.fonte.size(texto)
            texto = self.fonte.render(texto, False, pg.Color(255, 255, 255))
            meio = w/2 - tam_x/2
            canvas.blit(texto, (meio, y))

            y += barra_h + espaco

        pg.display.flip()

    def new(self):
        return self.janela if self.finalizado else self
