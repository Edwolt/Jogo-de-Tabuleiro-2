from tipos import board, movements, direction, coord

from .abc_peca import Peca
from .util import tabuleiro_false, calcula_direcao


class Bispo(Peca):
    def __init__(self, cor: bool):
        super().__init__(cor, nome='bispo')

    def get_movimentos_simples(self, tabuleiro: board, flags: list, pos: coord) -> movements:
        res = tabuleiro_false()
        direcoes = (
            direction(-1, 1),   # Cima Direita
            direction(-1, -1),  # Cima Esquerda
            direction(1, 1),    # Baixo Direita
            direction(1, -1),   # Baixo Esquerda
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
