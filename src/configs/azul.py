from pygame import Color, Surface
from pygame.font import Font


class Config:
    def __init__(self):
        self.vazio = Color(94, 255, 91), Color(0, 14, 173)
        self.click = Color(255, 0, 0)
        self.movimento = Color(0, 255, 255)
        self.background = Color(0, 0, 0)
        self.foreground = Color(255, 255, 255)

    def quadrado(self, canva: Surface, pos: tuple, tipo: str, complemento=None) -> None:
        i, j = pos

        cor = Color(0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento

        canva.fill(cor)

    def menu_fundo(self, canva: Surface) -> None:
        canva.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        return self.foreground

    def loading_cores(self) -> tuple:
        return Color(0, 255, 0), Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')

    def fonte(self, tam) -> Font:
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )
