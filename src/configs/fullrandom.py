from __future__ import annotations

from pygame import Color, Surface
from pygame.font import Font

from typing import NamedTuple
from random import randint

import tipos as tp
from abc_config import Config


def randcor() -> Color:
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))


class Nome(NamedTuple):
    titulo: str
    jogador: tp.pb[str]


class ConfigFullRandom(Config):
    def __init__(self):
        self.nomes = (
            Nome('Xadrez', tp.pb('Preto', 'Branco')),
            Nome('Jogo de Tabuleiro', tp.pb('Escuro', 'Claro')),
            Nome('Chess', tp.pb('Black', 'White')),
            Nome('Chess Game', tp.pb('Player 2', 'Player 1')),
        )

        self.vazio = tp.pb(randcor(), randcor())
        self.click = randcor()
        self.movimento = randcor()
        self.background = randcor()
        self.foreground = randcor()
        self.loading = randcor(), randcor()

        self.vez = True
        self.titulo_anterior = '.'

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
        res = tp.pb(
            tp.grad(randcor(), randcor()),
            tp.grad(randcor(), randcor())
        )
        res[False].tranparencia_padrao()
        res[True].tranparencia_padrao()

        return res

    def menu_fundo(self, canvas: Surface) -> None:
        canvas.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        return self.foreground

    def titulo(self, vez: bool) -> str:
        if self.vez != vez:
            self.vez = vez
            x, p = self.nomes[randint(0, len(self.nomes) - 1)]
            self.titulo_anterior = f'{x} : {p[vez]}'
            return f'{x} : {p[vez]}'
        else:
            return self.titulo_anterior

    def loading_cores(self) -> tuple[Color, Color]:
        return self.loading

    def fonte(self, tam) -> Font:
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )


export = ConfigFullRandom
