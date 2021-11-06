from pygame import transform
from pygame import Surface

from abc import ABC, abstractmethod

from recursos import Recursos
from tipos import matriz_tabuleiro, matriz_movimento, coord

from .xeque import testar_movimento
from .util import tabuleiro_false


class Peca(ABC):
    def __init__(self, cor: bool, *, nome: str):
        """
        :param sprite: Uma Surface com a imagem da peca
        :param cor: True: 'branco'; False: 'preto'
        """

        self.nome = nome
        self.cor = cor

    def draw(self, canvas: Surface) -> None:
        """
        Desenha o sprite em canvas
        :param canvas: Surface onde o jogo sera desenhado
        """

        recursos = Recursos()

        sprite = recursos.get_asset(self.nome, self.cor)
        sprite = transform.scale(sprite, canvas.get_size())
        canvas.blit(sprite, (0, 0))

    def notifica_movimento(self) -> None:
        """Notifica a peça que ela foi movimentada"""
        return

    @abstractmethod
    def get_movimentos_simples(self, tabuleiro: matriz_tabuleiro, flags: list, pos: coord) -> matriz_movimento:
        """
        :param flags: flags do tabuleiro
        :param pos: posição da peça, cujos movimentos estão sendo calculados
        :return: list 8x8 dizendo se é possivel movimentar ou não
        Caso o movimento seja especial é retornado um objeto de uma subclasse de MovimentoEspecial
        """

    def get_movimentos(self, tabuleiro: matriz_tabuleiro, flags: list, pos_rei: coord, pos: coord) -> matriz_movimento:
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
                    pos_rei, (pos, (i, j)),

                )
                res[i][j] = mov if teste else False
        return res
