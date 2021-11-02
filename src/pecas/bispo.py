from .abc_peca import Peca
from .util import tabuleiro_false, calcula_direcao


class Bispo(Peca):
    def __init__(self, cor: bool):
        super().__init__(cor, nome='bispo')

    def get_movimentos_simples(self, tabuleiro: list[list], flags: list, pos: tuple[int, int]) -> list[list]:
        res = tabuleiro_false()
        direcoes = (
            (-1, 1),   # Cima Direita
            (-1, -1),  # Cima Esquerda
            (1, 1),    # Baixo Direita
            (1, -1),   # Baixo Esquerda
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
