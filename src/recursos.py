from pygame import image
from pygame import Color, Surface

import importlib

from abc_config import Config


def get_config(nome: str) -> Config:
    module = importlib.import_module(f'configs.{nome.lower()}')
    return getattr(module, 'export')


def caminho_asset(nome: str, png_min: bool = False) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{nome}.png' + ('.min' if png_min else '')


class Recursos:
    def __init__(self, config: str, size: tuple[int, int] = (800, 800), framerate: int = 60, png_min: bool = False):
        self.size = size
        self.framerate = framerate
        self.png_min = png_min

        self.config = get_config(config)
        self.assets = dict()

    def set_config(self, config: str) -> None:
        self.config = get_config(config)

    def gerar_cor(self, grad: tuple[Color, Color], c: Color) -> Color:
        res = Color(0, 0, 0)
        a, b = grad
        for k in range(len(res)):
            res[k] = int(a[k] + (b[k] - a[k]) * (c[k] / 255))
        return res

    def gerar_imagem(self, sprite: Surface, grad_preto: tuple[Color, Color], grad_branco: tuple[Color, Color]) -> tuple[Surface, Surface]:
        preto = sprite.copy()
        branco = sprite.copy()
        w, h = sprite.get_size()

        for i in range(w):
            for j in range(h):
                cor = sprite.get_at((i, j))
                preto.set_at((i, j), self.gerar_cor(grad_preto, cor))
                branco.set_at((i, j), self.gerar_cor(grad_branco, cor))

        return preto, branco

    def carregar(self):
        """Carrega os assets das peças na memória"""
        nome_pecas = ['rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao']
        cores = self.config.pecas_cor()
        yield [(len(nome_pecas), 0)]
        for k, i in enumerate(nome_pecas):
            try:
                img = image.load(caminho_asset(i, self.png_min))
            except:
                img = image.load(caminho_asset(i))

            self.assets[i] = self.gerar_imagem(img, *cores)
            yield [(len(nome_pecas), k+1)]

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[nome][1 if cor else 0]
