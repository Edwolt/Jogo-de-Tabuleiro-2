from tipos import matriz_tabuleiro, matriz_movimento, coord

from .abc_peca import Peca
from .util import tabuleiro_false, calcula_direcao


class Bispo(Peca):
    def __init__(self, cor: bool):
        super().__init__(cor, nome='bispo')

    def get_movimentos_simples(self, tabuleiro: matriz_tabuleiro, flags: list, pos: coord) -> matriz_movimento:
        res = tabuleiro_false()
        direcoes = (
            (-1, 1),   # Cima Direita
            (-1, -1),  # Cima Esquerda
            (1, 1),    # Baixo Direita
            (1, -1),   # Baixo Esquerda
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
