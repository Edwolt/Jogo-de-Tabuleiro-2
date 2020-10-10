from pygame.event import Event
from pygame import Surface, Rect
from pygame import display, draw


class Loading():
    def __init__(self, janela):
        self.janela = janela
        self.load = self.janela.carregar()
        self.pronto = False

    def event(self, event: Event) -> None:
        pass

    # TODO Quando o draw for chamado carregar todos os itens e ir atualizando a Tela
    # Nesse caso o draw precisaria de outro nome
    def draw(self, canvas: Surface) -> None:
        vermelho = (255, 0, 0)
        verde = (0, 255, 0)

        canvas.fill((0, 0, 0))
        try:
            barras = next(self.load)
            print(barras)
        except StopIteration:
            print('pronto')
            self.pronto = True
            return

        w, h = canvas.get_size()
        y = 10
        x = 10

        for i in barras:
            tam, val = i
            bvermelho = Rect(x, y, (w - 2*x) * (val/tam), 15)
            bverde = Rect(x, y, w - 2*x, 15)
            draw.rect(canvas, verde, bverde)
            draw.rect(canvas, vermelho, bvermelho)
            display.flip()
            y += 20

    def new(self):
        if self.pronto:
            return self.janela
        else:
            return self
