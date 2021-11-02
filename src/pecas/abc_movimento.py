from abc import ABC, abstractmethod


class Movimento(ABC):
    """Classe abstrata para os movimentos especiais"""

    def __init__(self, *, nome: str):
        self.nome = nome

    @abstractmethod
    def executar(self, tabuleiro: list[list], flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """

    def update_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        return


class MovimentoEspecial(ABC):
    """Classe abstrata para os movimentos especiais"""

    def __init__(self, *, nome: str, avanco: bool = False):
        self.nome = nome
        self.avanco = avanco

    @abstractmethod
    def executar(self, tabuleiro: list[list], flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """

    def update_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        return
