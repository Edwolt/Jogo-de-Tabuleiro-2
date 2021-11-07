from pygame import Color, Surface
from pygame.font import Font

from abc_config import Config
from tipos import pb, coord, grad


class ConfigPadrao(Config):
    def __init__(self):
        self.vazio = pb(Color(0, 0, 0), Color(255, 255, 255))
        self.click = Color(255, 255, 0)
        self.movimento = Color(0, 255, 255)
        self.xeque = Color(255, 0, 0)
        self.background = Color(0, 0, 0)
        self.foreground = Color(255, 255, 255)

    def quadrado(self, canvas: Surface, pos: coord, tipo: str) -> None:
        i, j = pos

        cor = Color(0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2 == 0]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'especial':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento
        elif tipo == 'xeque':
            cor = self.xeque

        canvas.fill(cor)

    def pecas_cor(self) -> pb[grad]:
        return pb(
            grad(Color(0, 0, 0, 0), Color(100, 100, 100, 255)),
            grad(Color(100, 100, 100, 0), Color(255, 255, 255, 255))
        )

    def menu_fundo(self, canvas: Surface) -> None:
        canvas.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        return self.foreground

    def loading_cores(self) -> tuple[Color, Color]:
        return Color(0, 255, 0), Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        texto_cor = pb('Preto', 'Branco')
        return 'Xadrez : ' + texto_cor[vez]

    def fonte(self, tam) -> Font:
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )


export = ConfigPadrao
