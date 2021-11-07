from tipos import board, movements, coord, direction

from .abc_peca import Peca
from .util import tabuleiro_false, calcula_direcao


class Torre(Peca):
    def __init__(self, cor: bool, movimentou: bool = False):
        super().__init__(cor, nome='torre')
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def get_movimentos_simples(self, tabuleiro: board, flags: list, pos: coord) -> movements:
        res = tabuleiro_false()
        direcoes = (
            direction(-1, 0),  # Cima
            direction(1, 0),   # Baixo
            direction(0, -1),  # Esquerda
            direction(0, 1),   # Direita
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
