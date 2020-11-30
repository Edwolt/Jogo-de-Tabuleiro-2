from pygame import image
from pygame import Color, Surface

import importlib


def Config(nome: str):
    return importlib.import_module(f'configs.{nome}').Config()


def caminho_asset(nome: str) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{nome}.png'


def caminho_asset_min(nome: str) -> str:
    return f'assets/{nome}.png.min'


class Recursos:
    def __init__(self, config: str, size: tuple = (800, 800), framerate: int = 60, min=False):
        self.size = size
        self.framerate = framerate

        self.config = Config(config)
        self.assets = dict()

    def set_config(self, config: str) -> None:
        self.config = Config(config)

    def gerar_cor(self, grad: tuple, c: Color) -> Color:
        res = Color(0, 0, 0)
        a, b = grad
        for k in range(len(res)):
            res[k] = int(a[k] + (b[k] - a[k]) * (c[k] / 255))
        return res

    def gerar_imagem(self, sprite: Surface, grad_preto: tuple, grad_branco: tuple) -> tuple:
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
        yield [(len(nome_pecas), 0)]
        for k, i in enumerate(nome_pecas):
            self.assets[i] = self.gerar_imagem(
                image.load(caminho_asset_min(i) if min else caminho_asset(i)),
                (Color(0, 0, 0, 0), Color(100, 100, 100, 255)),
                (Color(100, 100, 100, 0), Color(255, 255, 255, 255))
            )
            yield [(len(nome_pecas), k+1)]

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[nome][1 if cor else 0]
