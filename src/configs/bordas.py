from pygame import Color, Surface, Rect
from pygame.font import Font
from pygame import draw


class Config:
    def __init__(self):
        self.vazio = Color(214, 165, 132), Color(124, 49, 0)
        self.click = Color(153, 0, 0)
        self.movimento = Color(229, 126, 0)
        self.xeque = Color(100, 0, 0)
        self.borda = Color(100, 100, 100)
        self.background = Color(0, 0, 0)
        self.foreground = Color(255, 255, 255)

    def quadrado(self, canva: Surface, pos: tuple[int, int], tipo: str) -> None:
        size = canva.get_size()
        quad = Rect(1, 1, size[0] - 2, size[1] - 2)

        canva.fill(self.borda)

        i, j = pos

        cor = Color(0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'especial':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento
        elif tipo == 'xeque':
            draw.rect(canva, self.vazio[(i+j) % 2], quad)
            draw.circle(
                canva,
                self.xeque,
                (canva.get_size()[0] / 2, canva.get_size()[0]/2),
                min(*canva.get_size())/3
            )
            return

        draw.rect(canva, cor, quad)

    def pecas_cor(self) -> tuple[tuple[Color, Color], tuple[Color, Color]]:
        return (
            (Color(0, 0, 0, 0), Color(100, 100, 100, 255)),
            (Color(100, 100, 100, 0), Color(255, 255, 255, 255))
        )

    def menu_fundo(self, canva: Surface) -> None:
        canva.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        return self.foreground

    def loading_cores(self) -> tuple[Color, Color]:
        return Color(0, 255, 0), Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')

    def fonte(self, tam) -> Font:
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )
