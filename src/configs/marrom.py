from __future__ import annotations

from pygame import Color, Surface
from pygame.font import Font

import tipos as tp
from abc_config import Config


class ConfigMarrom(Config):
    def __init__(self):
        self.vazio = tp.pb(Color(124, 49, 0), Color(214, 165, 132))
        self.click = Color(153, 0, 0)
        self.movimento = Color(229, 126, 0)
        self.background = Color(214, 165, 132)
        self.foreground = Color(124, 49, 0)

    def quadrado(self, canvas: Surface, pos: tp.coord, tipo: str) -> None:
        i, j = pos

        cor = Color(0, 0, 0)
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
            tp.grad(Color(0, 0, 0, 0), Color(100, 100, 100, 255)),
            tp.grad(Color(100, 100, 100, 0), Color(255, 255, 255, 255))
        )

    def menu_fundo(self, canvas: Surface) -> None:
        canvas.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        return self.foreground

    def loading_cores(self) -> tuple[Color, Color]:
        return Color(0, 255, 0), Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        texto_cor = tp.pb('Preto', 'Branco')
        return 'Xadrez : ' + texto_cor[vez]

    def fonte(self, tam) -> Font:
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )


export = ConfigMarrom
