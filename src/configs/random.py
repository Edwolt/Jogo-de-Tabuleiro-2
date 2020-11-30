from pygame import Color, Surface
from random import randint


def randcor() -> Color:
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))


class Config:
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
        self.background = Color(0, 0, 0)
        self.foreground = Color(255, 255, 255)

        self.vez = True
        self.titulo_anterior = '.'

    def quadrado(self, canva: Surface, pos: tuple, tipo: str, complemento=None) -> None:
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

        canva.fill(cor)

    def menu_fundo(self, canva: Surface) -> None:
        canva.fill(self.background)

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
