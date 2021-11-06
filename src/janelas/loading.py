from pygame.event import Event
from pygame import Color, Surface, Rect
from pygame import display, draw

from recursos import Recursos

from .abc_janela import Janela


class Loading(Janela):
    def __init__(self, carregamento, janela: Janela):
        self.janela = janela

        self.pronto = False
        self.carregamento = carregamento

        recursos = Recursos()
        self.fonte = recursos.config.fonte(25)
        self.fonte_loading = recursos.config.fonte(50)

    ##### Interface #####
    def event(self, event: Event) -> None:
        pass

    def draw(self, canvas: Surface) -> None:
        recursos = Recursos()
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
        texto = self.fonte_loading.render(texto, False, Color(255, 255, 255))
        meio = w/2 - tam_x/2
        canvas.blit(texto, (meio, y))

        y += tam_y + 2 * espaco

        for tam, val in barras:
            cor_carregado, cor_falta = recursos.config.loading_cores()
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
            texto = self.fonte.render(texto, False, Color(255, 255, 255))
            meio = w/2 - tam_x/2
            canvas.blit(texto, (meio, y))

            y += barra_h + espaco

        display.flip()

    def new(self):
        return self.janela if self.pronto else self
