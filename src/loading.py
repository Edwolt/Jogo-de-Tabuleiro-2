from pygame.event import Event
from pygame import Surface, Rect
from pygame import display, draw

from time import sleep
from random import randint


class Loading():
    def __init__(self, janela):
        self.janela = janela
        self.barras = [(1, 0)]
        self.pronto = False
        self.carregamento = self.janela.carregar()

    def event(self, event: Event) -> None:
        pass

    def carregar(self) -> None:
        for barras in self.janela.carregar():
            self.barras = barras

        self.barras = [(1, 1)]
        self.pronto = True

    # TODO Quando o draw for chamado carregar todos os itens e ir atualizando a Tela
    # Nesse caso o draw precisaria de outro nome

    def draw(self, canvas: Surface) -> None:

        cor_falta = 255, 0, 0
        cor_carregado = 0, 255, 0

        w, h = canvas.get_size()
        x = 10
        h = 15
        w = canvas.get_height() - 2 * x

        for barras in self.janela.carregar():
            canvas.fill((0, 0, 0))
            y = 10

            for i in barras:
                tam, val = i

                draw.rect(
                    canvas,
                    cor_falta,
                    Rect(x, y, w, h)
                )

                draw.rect(
                    canvas,
                    cor_carregado,
                    Rect(x, y, w * (val/tam), h)
                )

                display.flip()
                y += 20
            sleep(randint(0, 2))

        self.pronto = True

    def new(self):
        if self.pronto:
            return self.janela
        else:
            return self
