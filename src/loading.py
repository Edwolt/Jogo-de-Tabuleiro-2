from pygame.event import Event
from pygame import Color, Surface, Rect
from pygame import display, draw

from recursos import Recursos


class Loading():
    def __init__(self, recursos: Recursos, carregamento, janela):
        self.janela = janela
        self.pronto = False
        self.carregamento = carregamento

    def event(self, event: Event) -> None:
        pass

    def carregar(self) -> None:
        for barras in self.janela.carregar():
            self.barras = barras

        self.barras = [(1, 1)]
        self.pronto = True

    def draw(self, canvas: Surface) -> None:
        canvas.fill(Color(0, 0, 0))

        cor_falta = Color(255, 0, 0)
        cor_carregado = Color(0, 255, 0)

        x = 10
        y = 10
        h = 15
        w = canvas.get_height() - 2 * x

        try:
            barras = next(self.carregamento)
        except StopIteration:
            self.pronto = True
            return

        for tam, val in barras:
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
            y += 20

        display.flip()

    def new(self):
        return self.janela if self.pronto else self
