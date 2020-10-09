from pygame.event import Event
from pygame import Surface

class Loading():
    def __init__(self, janela):
        self.janela = janela
        pass

    def carregar(self) -> None:
        pass

    def event(self, event: Event) -> None:
        pass

    def draw(self, canvas: Surface) -> None:
        pass

    def new(self):
        self.janela.carregar()
        return self.janela
