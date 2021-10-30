from recursos import Recursos

from .abc_peca import Peca
from .util import tabuleiro_false, calcula_direcao


class Torre(Peca):
    def __init__(self,  recursos: Recursos, cor: bool, movimentou: bool = False):
        super().__init__(recursos, cor, nome='torre')
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def get_movimentos_simples(self, tabuleiro: list[list], flags: list, pos: tuple[int, int]) -> list[list]:
        res = tabuleiro_false()
        direcoes = (
            (-1, 0),  # Cima
            (1, 0),   # Baixo
            (0, -1),  # Esquerda
            (0, 1),   # Direita
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
