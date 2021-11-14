from __future__ import annotations

import pygame as pg
from abc import ABC, abstractmethod

import tipos as tp


class Config(ABC):
    @abstractmethod
    def quadrado(self, canvas: pg.Surface, pos: tp.coord, tipo: str) -> None:
        """
        Colore o quadrado que será usado em baixo da peça
        :param pos: Posição da peça
        :param tipo: Se tem algo especial no quadrado
        * vazio: Quadrado comum (pode estar ou não vazio)
        * click: Último quadrado que foi clicado
        * movimento: Quadrado disponível para movimentar
        * especial: Quadrado onde o movimento é especial
        * captura: Quadrado disponível para movimentar que resultará em um
        captura
        * xeque: Quadrado onde o rei está em xeque
        """

    @abstractmethod
    def pecas_cor(self) -> tp.pb[tp.grad]:
        """
        :return: pb(gradiente_preto, gradiente_branco)
        Retorna dois gradientes, um para colorir as peças brancas outro para as
        peças pretas
        """

    @abstractmethod
    def menu_fundo(self, canvas: pg.Surface) -> None:
        """Colore o fundo do menu (canvas)"""

    @abstractmethod
    def menu_opcao(self, opcao: str, selecionado: bool) -> tuple[str, pg.Color]:
        """
        :param opcao: O texto da opcao
        :param selecionado: Se a opção está selecionada
        :return: Cor que será usada na fonte para desenhar essa opção
        """

    @abstractmethod
    def loading_cores(self) -> tuple[pg.Color, pg.Color]:
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
    def fonte(self, tam: int) -> pg.font.Font:
        """
        :param tam: Tamanho da fonte
        :return: Objeto Font
        """
