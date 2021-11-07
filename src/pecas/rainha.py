from tipos import board, movements, coord, direction

from .abc_peca import Peca
from .util import tabuleiro_false, calcula_direcao


class Rainha(Peca):
    def __init__(self, cor: bool):
        super().__init__(cor, nome='rainha')

    def get_movimentos_simples(self, tabuleiro: board, flags: list, pos: coord) -> movements:
        res = tabuleiro_false()
        direcoes = (
            direction(-1, 0),   # Cima
            direction(1, 0),    # Baixo
            direction(0, -1),   # Esquerda
            direction(0, 1),    # Direita
            direction(-1, 1),   # Cima Direita
            direction(-1, -1),  # Cima Esquerda
            direction(1, 1),    # Baixo Direita
            direction(1, -1),   # Baixo Esquerda
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
