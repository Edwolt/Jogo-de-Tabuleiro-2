from __future__ import annotations

from abc import ABC, abstractmethod

import tipos as tp


class Movimento:
    """Classe abstrata para os movimentos especiais"""

    def __init__(self, acao: tp.action, rei: bool = False):
        self.acao = acao
        self.rei = rei

    def executar(self, tabuleiro: tp.board, flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """
        (i, j), (m, n) = self.acao

        tabuleiro[m][n] = tabuleiro[i][j]
        tabuleiro[i][j] = None
        tabuleiro[m][n].notifica_movimento()

    def atualiza_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        return


class MovimentoEspecial(ABC):
    """Classe abstrata para os movimentos especiais"""

    def __init__(self, *, nome: str, avanco: bool = False):
        self.nome = nome
        self.avanco = avanco

    @abstractmethod
    def executar(self, tabuleiro: tp.board, flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """

    def atualiza_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        return
