from pygame import Surface, Rect
from pygame import draw


class Config:
    def __init__(self):
        self.vazio = (
            (214, 165, 132),
            (124, 49, 0)
        )
        self.click = (153, 0, 0)
        self.movimento = (229, 126, 0)

    def quadrado(self, canva: Surface, pos: tuple, tipo: str, complemento=None) -> None:
        size = canva.get_size()
        quad = Rect(
            1, 1,
            size[0] - 2, size[1] - 2
        )

        canva.fill((100, 100, 100))

        i, j = pos

        cor = (0, 0, 0)
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
        canva.fill((0, 0, 0))

    def menu_cor(self, texto: str, selecionado: bool) -> tuple:
        return (255, 255, 255)

    def titulo(self, vez: bool) -> str:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')