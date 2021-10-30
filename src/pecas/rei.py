from pecas import Peca

from recursos import Recursos
from pecas import MovimentoEspecial
from pecas import testar_xeque
from .util import tabuleiro_copia, mover_peca


def valida_coordenadas(a: int, b: int = 0) -> bool:
    """
    valida_coordenada(a):    Verifica se a é um valor válido para componente de uma coordenada
    valida_coordenada(a, b): Verifica se (a, b) é uma coordenada válida
    """
    return 0 <= a < 8 and 0 <= b < 8


def tabuleiro_false() -> list[list[bool]]:
    """
    :return: list 8x8 com todos os campos sendo False
    """
    return [[False] * 8 for _ in range(8)]


class Roque(MovimentoEspecial):
    def __init__(self, rei: tuple[int, int], nova_rei: tuple[int, int], torre: tuple[int, int], nova_torre: tuple[int, int]):
        """
        :param rei: posição atual do rei
        :param nova_rei: posição para a qual o rei será movido
        :param torre: posição atual da torre
        :param nova_torre: posição para o qual a torre será movida
        """

        super().__init__(nome='roque')
        self.rei = rei
        self.nova_rei = nova_rei
        self.torre = torre
        self.nova_torre = nova_torre

    def executar(self, tabuleiro: list[list], flags: list, recursos: Recursos) -> None:
        mover_peca(tabuleiro, self.rei, self.nova_rei)
        mover_peca(tabuleiro, self.torre, self.nova_torre)


class Rei(Peca):
    def __init__(self, recursos: Recursos, cor: bool, movimentou: bool = False):
        super().__init__(recursos, cor, nome='rei')
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def valida_posicao(self, tabuleiro: list[list], pos: tuple[int, int]) -> bool:
        i, j = pos
        return tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

    def get_movimentos_simples(self, tabuleiro: list[list], flags: list, pos: tuple[int, int]) -> list[list]:
        # TODO Cuidado com cheque
        res = tabuleiro_false()
        i, j = pos

        # Casas acima do rei
        if valida_coordenadas(i-1, j-1):
            res[i-1][j-1] = self.valida_posicao(tabuleiro, (i-1, j-1))
        if valida_coordenadas(i-1, j):
            res[i-1][j] = self.valida_posicao(tabuleiro, (i-1, j))
        if valida_coordenadas(i-1, j+1):
            res[i-1][j+1] = self.valida_posicao(tabuleiro, (i-1, j+1))

        # Casas do meio
        if valida_coordenadas(i, j-1):
            res[i][j-1] = self.valida_posicao(tabuleiro, (i, j-1))
        if valida_coordenadas(i, j+1):
            res[i][j+1] = self.valida_posicao(tabuleiro, (i, j+1))

        # Casas abaixo do rei
        if valida_coordenadas(i+1, j-1):
            res[i+1][j-1] = self.valida_posicao(tabuleiro, (i+1, j-1))
        if valida_coordenadas(i+1, j):
            res[i+1][j] = self.valida_posicao(tabuleiro, (i+1, j))
        if valida_coordenadas(i+1, j+1):
            res[i+1][j+1] = self.valida_posicao(tabuleiro, (i+1, j+1))

        # Verifica se é possível fazer o Roque
        if not self.movimentou:
            torre = tabuleiro[i][0]
            if torre is not None and torre.nome == 'torre' and not torre.movimentou:
                # TODO verifica se deixa o rei em xeque ou passa em casas em xeque

                pecas_entre = False
                for jj in range(1, j):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                tab = tabuleiro_copia(tabuleiro)
                tab[i][3] = Rei(self.recursos, self.cor)
                tab[i][4] = None
                xeque = testar_xeque(tab, flags, (i, 3))

                if not xeque:
                    tab = tabuleiro_copia(tabuleiro)
                    tab[i][2] = Rei(self.recursos, self.cor)
                    tab[i][4] = None
                    xeque = testar_xeque(tab, flags, (i, 2))

                if not pecas_entre and not xeque:
                    res[i][j-2] = Roque((i, j), (i, j-2), (i, 0), (i, j-1))

            torre = tabuleiro[i][7]
            if torre is not None and torre.nome == 'torre' and not torre.movimentou:
                pecas_entre = False
                for jj in range(j + 1, 7):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                if not pecas_entre:
                    res[i][j+2] = Roque((i, j), (i, j+2), (i, 7), (i, j+1))

        return res
