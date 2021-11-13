from __future__ import annotations

import pygame as pg
from typing import NamedTuple
from random import randint

import tipos as tp
from abc_config import Config


def randcor() -> pg.Color:
    return pg.Color(randint(0, 255), randint(0, 255), randint(0, 255))


class Nome(NamedTuple):
    titulo: str
    jogador: tp.pb[str]


class ConfigUltimateRandom(Config):
    def __init__(self):
        self.nomes = (
            Nome('Xadrez', tp.pb('Preto', 'Branco')),
            Nome('Jogo de Tabuleiro', tp.pb('Escuro', 'Claro')),
            Nome('Chess', tp.pb('Black', 'White')),
            Nome('Chess Game', tp.pb('Player 2', 'Player 1')),
        )

        self.vez = None
        self.titulo_anterior = '.'

    def quadrado(self, canvas: pg.Surface, pos: tp.coord, tipo: str) -> None:
        canvas.fill(randcor())

    def pecas_cor(self) -> tp.pb[tp.grad]:
        res = tp.pb(
            tp.grad(randcor(), randcor()),
            tp.grad(randcor(), randcor())
        )
        res.preto.transparencia_padrao()
        res.branco.transparencia_padrao()

        return res

    def menu_fundo(self, canvas: pg.Surface) -> None:
        canvas.fill(randcor())

    def menu_cor(self, selecionado: bool) -> pg.Color:
        return randcor()

    def loading_cores(self) -> tuple[pg.Color, pg.Color]:
        return randcor(), randcor()

    def titulo(self, vez: bool) -> str:
        if self.vez is None or self.vez != vez:
            self.vez = vez
            x, p = self.nomes[randint(0, len(self.nomes) - 1)]
            self.titulo_anterior = f'{x} : {p[vez]}'
            return f'{x} : {p[vez]}'
        else:
            return self.titulo_anterior

    def fonte(self, tam) -> pg.font.Font:
        return pg.font.Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )


export = ConfigUltimateRandom
