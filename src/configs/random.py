from pygame import Color, Surface
from pygame.font import Font

from random import randint
from typing import NamedTuple

from abc_config import Config
from tipos import pb, coord, grad


def randcor() -> Color:
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))


class Nome(NamedTuple):
    titulo: str
    jogador: pb[str]


class ConfigRandom(Config):
    def __init__(self):
        self.nomes = (
            Nome('Xadrez', pb('Preto', 'Branco')),
            Nome('Jogo de Tabuleiro', pb('Escuro', 'Claro'), ),
            Nome('Chess', pb('Black', 'White')),
            Nome('Chess Game', pb('Player 2', 'Player 1')),
        )

        self.vazio = pb(randcor(), randcor())
        self.click = randcor()
        self.movimento = randcor()
        self.background = Color(0, 0, 0)
        self.foreground = Color(255, 255, 255)

        self.vez = True
        self.titulo_anterior = '.'

    def quadrado(self, canvas: Surface, pos: coord, tipo: str) -> None:
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

    def pecas_cor(self) -> pb[grad]:
        return pb(
            grad(Color(0, 0, 0, 0), Color(100, 100, 100, 255)),
            grad(Color(100, 100, 100, 0), Color(255, 255, 255, 255))
        )

    def menu_fundo(self, canvas: Surface) -> None:
        canvas.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        return self.foreground

    def loading_cores(self) -> tuple[Color, Color]:
        return Color(0, 255, 0), Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        if self.vez != vez:
            self.vez = vez
            x, p = self.nomes[randint(0, len(self.nomes) - 1)]
            self.titulo_anterior = f'{x} : {p[vez]}'
            return f'{x} : {p[vez]}'
        else:
            return self.titulo_anterior

    def fonte(self, tam) -> Font:
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )


export = ConfigRandom
