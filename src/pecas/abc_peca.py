from __future__ import annotations

from pygame import transform
from pygame import Surface

from abc import ABC, abstractmethod

import tipos as tp
import recursos as rsc  # Para evitar circular import

from .xeque import testar_movimento
from .util import tabuleiro_false


class Peca(ABC):
    def __init__(self, cor: bool, *, nome: str):
        """
        :param nome: O nome da peça
        :param cor: False: 'preto'; True: 'branco'
        """

        self.nome = nome
        self.cor = cor

    def draw(self, canvas: Surface) -> None:
        """
        Desenha a peça no canvas
        :param canvas: Surface onde o jogo sera desenhado
        """

        recursos = rsc.Recursos()

        sprite = recursos.get_asset(self.nome, self.cor)
        sprite = transform.scale(sprite, canvas.get_size())
        canvas.blit(sprite, (0, 0))

    def notifica_movimento(self) -> None:
        """Notifica a peça que ela foi movimentada"""
        return

    @abstractmethod
    def get_movimentos_simples(self, tabuleiro: tp.board, flags: list, pos: tp.coord) -> tp.movements:
        """
        :param flags: flags do tabuleiro
        :param pos: posição da peça, cujos movimentos estão sendo calculados
        :return: matriz movements com todos os movimentos possíveis, porém contendo movimentos ilegais que causam xeque
        """

    def get_movimentos(self, tabuleiro: tp.board, flags: list, pos_rei: tp.coord, pos: tp.coord) -> tp.movements:
        """
        :param flags: flags do tabuleiro
        :param pos: posição da peça, cujos movimentos estão sendo calculados
        :return: matriz movements com todos os movimentos legais
        """

        res = tabuleiro_false()
        movimentos = self.get_movimentos_simples(tabuleiro, flags, pos)
        for i, linha in enumerate(movimentos):
            for j, mov in enumerate(linha):
                teste = testar_movimento(
                    tabuleiro, flags,
                    pos_rei, tp.action(pos, tp.coord(i, j)),
                )
                res[i][j] = mov if teste else False
        return res
