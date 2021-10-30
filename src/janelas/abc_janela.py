from pygame.event import Event
from pygame import Surface

from abc import ABC, abstractmethod


class Janela(ABC):
    @abstractmethod
    def event(self, event: Event) -> None:
        """
        Recebe um evento e executa uma operação com ele
        :param event: evento
        """

    @abstractmethod
    def draw(self, canvas: Surface) -> None:
        """
        :param canvas: Surface onde o jogo sera desenhado
        :return: Retorna se a tela precisa ser atualizada
        """

    @abstractmethod
    def new(self) -> 'Janela':
        """
        Create
        """
