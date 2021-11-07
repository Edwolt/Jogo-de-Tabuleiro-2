from abc import ABC, abstractmethod

from tipos import matriz_tabuleiro, mov


class Movimento:
    """Classe abstrata para os movimentos especiais"""

    def __init__(self, movimento: mov, rei: bool = False):
        self.movimento = movimento
        self.rei = rei

    def executar(self, tabuleiro: matriz_tabuleiro, flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """
        (i, j), (m, n) = self.movimento

        tabuleiro[m][n] = tabuleiro[i][j]
        tabuleiro[i][j] = None
        tabuleiro[m][n].notifica_movimento()

    def update_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        return


class MovimentoEspecial(ABC):
    """Classe abstrata para os movimentos especiais"""

    def __init__(self, *, nome: str, avanco: bool = False):
        self.nome = nome
        self.avanco = avanco

    @abstractmethod
    def executar(self, tabuleiro: matriz_tabuleiro, flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """

    def update_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        return
