from pygame.event import Event
from pygame import Color, Surface, Rect
from pygame import display, draw

from recursos import Recursos


class Loading():
    def __init__(self, recursos: Recursos, carregamento, janela):
        self.janela = janela
        self.pronto = False
        self.carregamento = carregamento
        self.fonte = recursos.config.fonte(25)

    def event(self, event: Event) -> None:
        pass

    def draw(self, canvas: Surface) -> None:
        canvas.fill(Color(0, 0, 0))

        cor_falta = Color(255, 0, 0)
        cor_carregado = Color(0, 255, 0)

        x = 10
        y = 10
        espaco = 10
        h = self.fonte.size('')[1]
        w = canvas.get_width() - 2 * x

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

            texto = f'{val} / {tam}'
            xx, yy = self.fonte.size(texto)
            meio = canvas.get_width() / 2 - xx
            texto = self.fonte.render(texto, 0, Color(255, 255, 255))
            canvas.blit(texto, (meio, y))


            y += yy + espaco

        display.flip()

    def new(self):
        return self.janela if self.pronto else self
