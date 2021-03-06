from pygame.event import Event
from pygame import Color, Surface, Rect
from pygame import display, draw

from recursos import Recursos


class Loading():
    def __init__(self, recursos: Recursos, carregamento, janela):
        self.janela = janela
        self.recursos = recursos

        self.pronto = False
        self.carregamento = carregamento

        self.fonte = self.recursos.config.fonte(25)
        self.fonte_loading = recursos.config.fonte(50)

    def event(self, event: Event) -> None:
        pass

    def draw(self, canvas: Surface) -> None:
        canvas.fill(Color(0, 0, 0))

        try:
            barras = next(self.carregamento)
        except StopIteration:
            self.pronto = True
            return

        x, y = 10, 10
        espaco = 10
        w = canvas.get_size()[0]
        barra_w, barra_h = w - 2 * x, 30

        texto = 'Loading'
        tam_x, tam_y = self.fonte_loading.size(texto)
        texto = self.fonte_loading.render(texto, 0, Color(255, 255, 255))
        meio = w/2 - tam_x/2
        canvas.blit(texto, (meio, y))

        y += tam_y + 2 * espaco

        for tam, val in barras:
            cor_carregado, cor_falta = self.recursos.config.loading_cores()
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

            y += barra_h + espaco

        display.flip()

    def new(self):
        return self.janela if self.pronto else self
