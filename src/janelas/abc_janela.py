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
        """:param canvas: Surface onde o jogo sera desenhado"""

    @abstractmethod
    def new(self) -> 'Janela':
        """
        Diz qual a janela a ser exibida no próximo frame
        Para continuar na mesma janela basta retorna ela mesma
        """
