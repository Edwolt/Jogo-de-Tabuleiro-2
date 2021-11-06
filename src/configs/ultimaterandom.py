from pygame import Color, Surface
from pygame.font import Font

from random import randint

from abc_config import Config
from tipos import coord, grad


def randcor() -> Color:
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))


class ConfigUltimateRandom(Config):
    def __init__(self):
        self.nomes = (
            ('Xadrez', 'Branco', 'Preto'),
            ('Jogo de Tabuleiro', 'Claro', 'Escuro'),
            ('Chess', 'White', 'Black'),
            ('Chess Game', 'Player 1', 'Player 2'),
        )

        self.vez = None
        self.titulo_anterior = '.'

    def quadrado(self, canvas: Surface, pos: coord, tipo: str) -> None:
        canvas.fill(randcor())

    def pecas_cor(self) -> tuple[grad, grad]:
        res = (randcor(), randcor()), (randcor(), randcor())
        res[0][0].a = 0
        res[0][1].a = 255
        res[1][0].a = 0
        res[1][1].a = 255

        return res

    def menu_fundo(self, canvas: Surface) -> None:
        canvas.fill(randcor())

    def menu_cor(self, selecionado: bool) -> Color:
        return randcor()

    def loading_cores(self) -> tuple[Color, Color]:
        return randcor(), randcor()

    def titulo(self, vez: bool) -> str:
        if self.vez is None or self.vez != vez:
            self.vez = vez
            x, p1, p2 = self.nomes[randint(0, len(self.nomes) - 1)]
            p = p1 if vez else p2
            self.titulo_anterior = f'{x} : {p}'
            return f'{x} : {p}'
        else:
            return self.titulo_anterior

    def fonte(self, tam) -> Font:
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )


export = ConfigUltimateRandom
