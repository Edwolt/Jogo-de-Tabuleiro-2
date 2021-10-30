from pygame import transform
from pygame import Surface

from abc import ABC, abstractmethod

from recursos import Recursos
from pecas import MovimentoEspecial
from pecas import testar_xeque
from .util import tabuleiro_copia


def tabuleiro_false() -> list[list[bool]]:
    """
    :return: list 8x8 com todos os campos sendo False
    """
    return [[False] * 8 for _ in range(8)]


# TODO pode ser muito otimizado
def testar_movimento(tabuleiro: list[list], flags: list, recursos: Recursos, pos_rei: tuple[int, int], acao: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    tab = tabuleiro_copia(tabuleiro)
    pos, nova_pos = acao
    i, j = pos
    m, n = nova_pos
    movimento = tab[i][j].get_movimentos_simples(tab, flags, pos)[m][n]

    # Movimenta peca
    if isinstance(movimento, bool) and movimento:
        tab[m][n] = tabuleiro[i][j]
        tab[i][j] = None
        tab[m][n].notifica_movimento()

        if pos_rei == pos:
            pos_rei = nova_pos

        flags.clear()

    elif isinstance(movimento, MovimentoEspecial):
        movimento.executar(tab, flags, recursos)

        if movimento.nome == 'roque' and pos_rei == movimento.rei:
            pos_rei = movimento.nova_rei

        flags.clear()
        movimento.update_flags(flags)
    else:
        return False

    # Testa Xeque
    return not testar_xeque(tab, flags, pos_rei)


class Peca(ABC):
    def __init__(self, recursos: Recursos, cor: bool, *, nome: str):
        """
        :param sprite: Uma Surface com a imagem da peca
        :param cor: True: 'branco'; False: 'preto'
        """

        self.nome = nome
        self.recursos = recursos
        self.cor = cor

    def draw(self, canvas: Surface) -> None:
        """
        Desenha o sprite em canvas
        :param canvas: Surface onde o jogo sera desenhado
        """
        sprite = self.recursos.get_asset(self.nome, self.cor)
        sprite = transform.scale(sprite, canvas.get_size())
        canvas.blit(sprite, (0, 0))

    def notifica_movimento(self) -> None:
        """Notifica a peça que ela foi movimentada"""
        return

    @abstractmethod
    def get_movimentos_simples(self, tabuleiro: list[list], flags: list, pos: tuple[int, int]) -> list[list]:
        """
        :param flags: flags do tabuleiro
        :param pos: posição da peça, cujos movimentos estão sendo calculados
        :return: list 8x8 dizendo se é possivel movimentar ou não
        Caso o movimento seja especial é retornado um objeto de uma subclasse de MovimentoEspecial
        """

    def get_movimentos(self, tabuleiro: list[list], flags: list, pos_rei: tuple[int, int], pos: tuple[int, int]) -> list[list]:
        """
        :param flags: flags do tabuleiro
        :param pos: posição da peça, cujos movimentos estão sendo calculados
        :return: list 8x8 dizendo se é possivel movimentar ou não
        Caso o movimento seja especial é retornado um objeto de uma subclasse de MovimentoEspecial
        """
        res = tabuleiro_false()
        movimentos = self.get_movimentos_simples(tabuleiro, flags, pos)
        for i, linha in enumerate(movimentos):
            for j, mov in enumerate(linha):
                teste = testar_movimento(
                    tabuleiro, flags,
                    self.recursos,
                    pos_rei, (pos, (i, j)),

                )
                res[i][j] = mov if teste else False
        return res
