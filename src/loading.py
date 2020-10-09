from pygame.event import Event
from pygame import Surface


class Loading():
    def __init__(self, janela):
        self.janela = janela
        pass

    def event(self, event: Event) -> None:
        pass

    # TODO Quando o draw for chamado carregar todos os itens e ir atualizando a Tela
    # Nesse caso o draw precisaria de outro nome
    def draw(self, canvas: Surface) -> None:
        pass

    def new(self):
        self.janela.carregar()
        return self.janela
