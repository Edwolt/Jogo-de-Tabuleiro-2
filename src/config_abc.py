from pygame import Color, Surface
from pygame.font import Font

from abc import ABC, abstractmethod


class Config(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def quadrado(self, canvas: Surface, pos: tuple[int, int], tipo: str) -> None:
        """
        Colore o quadrado que será usado em baixo da peça
        :param pos: Posição da peça
        :param tipo: Se tem algo especial no quadrado
        * vazio: Quadrado comum (pode estar ou não vazio)
        * click: Último quadrado que foi clicado
        * movimento: Quadrado disponível para movimentar
        * especial: Quadrado onde o movimento é especial
        * captura: Quadrado disponível para movimentar que resultará em um captura
        * xeque: Quadrado onde o rei está em xeque
        """

    @abstractmethod
    def pecas_cor(self) -> tuple[tuple[Color, Color], tuple[Color, Color]]:
        """
        :return: (gradiente_branco, gradiente_preto)
        Retorna dois gradientes, um para colorir as peças brancas outro para as peças pretas
        """

    @abstractmethod
    def menu_fundo(self, canvas: Surface) -> None:
        """Colore o fundo do menu (canvas)"""

    @abstractmethod
    def menu_cor(self, selecionado: bool) -> Color:
        """
        :param texto: Texto da opção
        :param selecionado: Se a opção está selecionada
        :return: Cor que será usada na fonte para desenhar essa opção
        """

    @abstractmethod
    def loading_cores(self) -> tuple[Color, Color]:
        """
        :returns: Retorna uma tupla de cores para desenhar as barras de loading
        A primeira cor é usada para mostrar o que já foi carregado
        e a segunda o quanto falta
        """

    @abstractmethod
    def titulo(self, vez: bool) -> str:
        """
        :param vez: Qual turno o jogo está
        :return: O título que será usado para a janela
        """

    @abstractmethod
    def fonte(self, tam) -> Font:
        """
        :param tam: Tamanho da fonte
        :return: Objeto Font
        """