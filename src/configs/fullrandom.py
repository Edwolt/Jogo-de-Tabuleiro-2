from pygame import Color, Surface
from pygame.font import Font

from random import randint

from abc_config import Config


def randcor() -> Color:
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))


class ConfigFullRandom(Config):
    def __init__(self):
        self.nomes = (
            ('Xadrez', 'Branco', 'Preto'),
            ('Jogo de Tabuleiro', 'Claro', 'Escuro'),
            ('Chess', 'White', 'Black'),
            ('Chess Game', 'Player 1', 'Player 2'),
        )

        self.vazio = randcor(), randcor()
        self.click = randcor()
        self.movimento = randcor()
        self.background = randcor()
        self.foreground = randcor()
        self.loading = randcor(), randcor()

        self.vez = True
        self.titulo_anterior = '.'

    def quadrado(self, canvas: Surface, pos: tuple[int, int], tipo: str) -> None:
        i, j = pos

        cor = Color(0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento

        canvas.fill(cor)

    def pecas_cor(self) -> tuple[tuple[Color, Color], tuple[Color, Color]]:
        res = (randcor(), randcor()), (randcor(), randcor())
        res[0][0].a = 0
        res[0][1].a = 255
        res[1][0].a = 0
        res[1][1].a = 255

        return res

    def menu_fundo(self, canvas: Surface) -> None:
        canvas.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        return self.foreground

    def titulo(self, vez: bool) -> str:
        if self.vez != vez:
            self.vez = vez
            x, p1, p2 = self.nomes[randint(0, len(self.nomes) - 1)]
            p = p1 if vez else p2
            self.titulo_anterior = f'{x} : {p}'
            return f'{x} : {p}'
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
