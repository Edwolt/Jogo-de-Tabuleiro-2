from pygame.event import Event
from pygame import Surface, Rect
from pygame import display, draw


class Loading():
    def __init__(self, janela):
        self.janela = janela
        self.carregamento = self.janela.carregar()
        self.pronto = False

    def event(self, event: Event) -> None:
        pass

    # TODO Quando o draw for chamado carregar todos os itens e ir atualizando a Tela
    # Nesse caso o draw precisaria de outro nome
    def draw(self, canvas: Surface) -> None:
        canvas.fill((0, 0, 0))

        cor_falta = (255, 0, 0)
        cor_carregado = (0, 255, 0)

        try:
            barras = next(self.carregamento)
        except StopIteration:
            self.pronto = True
            return

        w, h = canvas.get_size()
        y = 10
        x = 10
        h = 15
        w = canvas.get_height() - 2*x

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

    def new(self):
        if self.pronto:
            return self.janela
        else:
            return self
