from pygame import image
from pygame import Color, Surface

import importlib

from singleton import Singleton
from abc_config import Config
from tipos import grad


def get_config(nome: str) -> Config:
    module = importlib.import_module(f'configs.{nome.lower()}')
    cls = getattr(module, 'export')
    return cls()


def caminho_asset(nome: str, png_min: bool = False) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{nome}.png' + ('.min' if png_min else '')


class Recursos(metaclass=Singleton):
    def __init__(self, size: tuple[int, int] = (800, 800), framerate: int = 60, png_min: bool = False):
        self.size = size
        self.framerate = framerate
        self.png_min = png_min

        self._config = None
        self.assets = dict()

    @property
    def config(self) -> Config:
        if self._config is None:
            raise Exception('Nenhum config foi carregada')
        return self._config

    @config.deleter
    def config(self):
        self._config = None

    def set_config(self, config: str) -> None:
        self._config = get_config(config)

    def gerar_cor(self, gradiente: grad, c: Color) -> Color:
        res = Color(0, 0, 0)
        a, b = gradiente
        for k in range(len(res)):
            res[k] = int(a[k] + (b[k] - a[k]) * (c[k] / 255))
        return res

    def gerar_imagem(self, sprite: Surface, grad_preto: grad, grad_branco: grad) -> tuple[Surface, Surface]:
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
