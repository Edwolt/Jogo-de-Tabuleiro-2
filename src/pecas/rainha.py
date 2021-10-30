from recursos import Recursos
from pecas import Peca
from .util import tabuleiro_false, calcula_direcao


class Rainha(Peca):
    def __init__(self, recursos: Recursos, cor: bool):
        super().__init__(recursos, cor, nome='rainha')
        self.nome = 'rainha'
        self.recursos = recursos
        self.cor = cor

    def get_movimentos_simples(self, tabuleiro: list[list], flags: list, pos: tuple[int, int]) -> list[list]:
        res = tabuleiro_false()
        direcoes = (
            (-1, 0),   # Cima
            (1, 0),    # Baixo
            (0, -1),   # Esquerda
            (0, 1),    # Direita
            (-1, 1),   # Cima Direita
            (-1, -1),  # Cima Esquerda
            (1, 1),    # Baixo Direita
            (1, -1),   # Baixo Esquerda
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
