from pygame import Color, Surface, Rect
from pygame import draw


class Config:
    def __init__(self):
        self.vazio = Color(214, 165, 132), Color(124, 49, 0)
        self.click = Color(153, 0, 0)
        self.movimento = Color(229, 126, 0)

    def quadrado(self, canva: Surface, pos: tuple, tipo: str, complemento=None) -> None:
        size = canva.get_size()
        quad: Rect = Rect(
            1, 1,
            size[0] - 2, size[1] - 2
        )

        canva.fill(Color(100, 100, 100))

        i, j = pos

        cor = 0, 0, 0
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento

        draw.rect(canva, cor, quad)

    def menu_fundo(self, canva: Surface) -> None:
        canva.fill(Color(0, 0, 0))

    def menu_cor(self, texto: str, selecionado: bool) -> Color:
        return Color(255, 255, 255)

    def titulo(self, vez: bool) -> str:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')
