from __future__ import annotations

import pygame as pg

import tipos as tp
from abc_config import Config


class ConfigMarrom(Config):
    def __init__(self):
        self.vazio = tp.pb(pg.Color(124, 49, 0), pg.Color(214, 165, 132))
        self.click = pg.Color(153, 0, 0)
        self.movimento = pg.Color(229, 126, 0)
        self.background = pg.Color(214, 165, 132)
        self.foreground = pg.Color(124, 49, 0)

    def quadrado(self, canvas: pg.Surface, pos: tp.coord, tipo: str) -> None:
        i, j = pos

        cor = pg.Color(0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2 == 0]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento

        canvas.fill(cor)

    def pecas_cor(self) -> tp.pb[tp.grad]:
        return tp.pb(
            tp.grad(pg.Color(0, 0, 0, 0), pg.Color(100, 100, 100, 255)),
            tp.grad(pg.Color(100, 100, 100, 0), pg.Color(255, 255, 255, 255))
        )

    def menu_fundo(self, canvas: pg.Surface) -> None:
        canvas.fill(self.background)

    def menu_cor(self, selecionado: bool) -> pg.Color:
        return self.foreground

    def loading_cores(self) -> tuple[pg.Color, pg.Color]:
        return pg.Color(0, 255, 0), pg.Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        texto_cor = tp.pb('Preto', 'Branco')
        return 'Xadrez : ' + texto_cor[vez]

    def fonte(self, tam) -> pg.font.Font:
        return pg.font.Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )


export = ConfigMarrom
