from tipos import board, movements, coord

from .abc_peca import Peca
from .util import tabuleiro_false


class Cavalo(Peca):
    def __init__(self, cor: bool):
        super().__init__(cor, nome='cavalo')

    def valida_posicao(self, tabuleiro: board, pos: coord) -> bool:
        i, j = pos
        return tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

    def get_movimentos_simples(self, tabuleiro: board, flags: list, pos: coord) -> movements:
        res = tabuleiro_false()
        i, j = pos

        # Casas acima
        if coord(i-2, j-1).valida:
            res[i-2][j-1] = self.valida_posicao(tabuleiro, coord(i-2, j-1))
        if coord(i-2, j+1).valida:
            res[i-2][j+1] = self.valida_posicao(tabuleiro, coord(i-2, j+1))

        # Casas abaixo
        if coord(i+2, j-1).valida:
            res[i+2][j-1] = self.valida_posicao(tabuleiro, coord(i+2, j-1))
        if coord(i+2, j+1).valida:
            res[i+2][j+1] = self.valida_posicao(tabuleiro, coord(i+2, j+1))

        # Casas a esquerda
        if coord(i-1, j-2).valida:
            res[i-1][j-2] = self.valida_posicao(tabuleiro, coord(i-1, j-2))
        if coord(i+1, j-2).valida:
            res[i+1][j-2] = self.valida_posicao(tabuleiro, coord(i+1, j-2))

        # Casas a direira
        if coord(i-1, j+2).valida:
            res[i-1][j+2] = self.valida_posicao(tabuleiro, coord(i-1, j+2))
        if coord(i+1, j+2).valida:
            res[i+1][j+2] = self.valida_posicao(tabuleiro, coord(i+1, j+2))

        return res
