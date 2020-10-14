from pygame import Surface
from random import randint


def randcor() -> tuple:
    return randint(0, 255), randint(0, 255), randint(0, 255)


class Config:
    def __init__(self):
        self.nomes = (
            ('Xadrez', 'Branco', 'Preto'),
            ('Jogo de Tabuleiro', 'Claro', 'Escuro'),
            ('Chess', 'White', 'Black'),
            ('Chess Game', 'Player 1', 'Player 2'),
        )

        self.vez = True
        self.titulo_anterior = '.'

    def quadrado(self, canva: Surface, pos: tuple, tipo: str, complemento=None) -> None:
        canva.fill(randcor())

    def menu_fundo(self, canva: Surface) -> None:
        canva.fill(randcor())

    def menu_cor(self, texto: str, selecionado: bool) -> tuple:
        return randcor()

    def titulo(self, vez: bool) -> str:
        if self.vez != vez:
            self.vez = vez
            x, p1, p2 = self.nomes[randint(0, len(self.nomes) - 1)]
            p = p1 if vez else p2
            self.titulo_anterior = f'{x} : {p}'
            return f'{x} : {p}'
        else:
            return self.titulo_anterior
