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
        self.fonte_loading = recursos.config.fonte(50)

    def event(self, event: Event) -> None:
        pass

    def draw(self, canvas: Surface) -> None:
        canvas.fill(Color(0, 0, 0))

        cor_falta = Color(255, 0, 0)
        cor_carregado = Color(0, 255, 0)

        try:
            barras = next(self.carregamento)
        except StopIteration:
            self.pronto = True
            return

        x, y = 10, 10
        espaco = 10
        w, h = self.fonte.size('')
        barra_w, barra_h = w - 2 * x, h

        texto = 'Loading'
        tam_x, tam_y = self.fonte_loading.size(texto)
        texto = self.fonte_loading.render(texto, 0, Color(255, 255, 255))
        meio = w/2 - tam_x/2
        canvas.blit(texto, (meio, y))

        y += tam_y + 2 * espaco

        for tam, val in barras:
            draw.rect(
                canvas,
                cor_falta,
                Rect(x, y, barra_w, barra_h)
            )
            draw.rect(
                canvas,
                cor_carregado,
                Rect(x, y, barra_w * (val/tam), barra_h)
            )

            texto = f'{val} / {tam}'
            tam_x, tam_y = self.fonte.size(texto)
            texto = self.fonte.render(texto, 0, Color(255, 255, 255))
            meio = w/2 - tam_x/2
            canvas.blit(texto, (meio, y))

            y += tam_y + espaco

        display.flip()

    def new(self):
        return self.janela if self.pronto else self
