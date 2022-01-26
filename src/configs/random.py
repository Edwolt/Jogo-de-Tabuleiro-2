from __future__ import annotations

import pygame as pg
from typing import NamedTuple
from random import randint

import tipos as tp


def randcor() -> pg.Color:
    return pg.Color(randint(0, 255), randint(0, 255), randint(0, 255))


class Nome(NamedTuple):
    titulo: str
    jogador: tp.pb[str]


class ConfigRandom:
    def __init__(self):
        self.nomes = (
            Nome("Xadrez", tp.pb("Preto", "Branco")),
            Nome("Jogo de Tabuleiro", tp.pb("Escuro", "Claro")),
            Nome("Chess", tp.pb("Black", "White")),
            Nome("Chess Game", tp.pb("Player 2", "Player 1")),
        )

        self.vazio = tp.pb(randcor(), randcor())
        self.click = randcor()
        self.movimento = randcor()
        self.background = pg.Color(0, 0, 0)
        self.foreground = pg.Color(255, 255, 255)

        self.vez = True
        self.titulo_anterior = "."

    def quadrado(self, canvas: pg.Surface, pos: tp.coord, tipo: str) -> None:
        i, j = pos

        match tipo:
            case "vazio":
                cor = self.vazio[(i + j) % 2 == 0]
            case "click":
                cor = self.click
            case "movimento" | "captura":
                cor = self.movimento
            case _:
                cor = pg.Color(0, 0, 0)

        canvas.fill(cor)

    def pecas_cor(self) -> tp.pb[tp.grad]:
        return tp.pb(
            tp.grad(pg.Color(0, 0, 0, 0), pg.Color(100, 100, 100, 255)),
            tp.grad(pg.Color(100, 100, 100, 0), pg.Color(255, 255, 255, 255)),
        )

    def menu_fundo(self, canvas: pg.Surface) -> None:
        canvas.fill(self.background)

    def menu_opcao(self, opcao: str, selecionado: bool) -> tuple[str, pg.Color]:
        if selecionado:
            opcao = "> " + opcao
        else:
            opcao = "  " + opcao

        return opcao, self.foreground

    def loading_cores(self) -> tuple[pg.Color, pg.Color]:
        return pg.Color(0, 255, 0), pg.Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        if self.vez != vez:
            self.vez = vez
            x, p = self.nomes[randint(0, len(self.nomes) - 1)]
            self.titulo_anterior = f"{x} : {p[vez]}"
            return f"{x} : {p[vez]}"
        else:
            return self.titulo_anterior

    def fonte(self, tam) -> pg.font.Font:
        return pg.font.Font(
            "assets/inconsolata/static/Inconsolata-Medium.ttf", tam
        )


export = ConfigRandom
