from __future__ import annotations

from pygame import image
from pygame import Surface

import importlib

import tipos as tp
from abc_config import Config
from singleton import Singleton


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

    def gerar_imagem(self, sprite: Surface, gradientes: tp.pb[tp.grad]) -> tp.pb[Surface]:
        """
        Colore o sprite com os gradientes e os retorna
        :param sprite: sprite a ser colorido
        :param gradientes: gradientes para a peça preta e branca
        :return: sprites coloridos para a peça preta e para branca
        """
        sprites = tp.pb(sprite.copy(), sprite.copy())
        w, h = sprite.get_size()

        for i in range(w):
            for j in range(h):
                cor = sprite.get_at((i, j))
                sprites[False].set_at((i, j), gradientes[False].gerar_cor(cor))
                sprites[True].set_at((i, j), gradientes[True].gerar_cor(cor))

        return sprites

    def carregar(self) -> tp.load_gen:
        """Carrega os assets das peças na memória"""
        nome_pecas = ['rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao']
        cores = self.config.pecas_cor()
        yield [tp.load_bar(len(nome_pecas), 0)]
        for k, i in enumerate(nome_pecas):
            try:
                img = image.load(caminho_asset(i, self.png_min))
            except:
                img = image.load(caminho_asset(i))

            self.assets[i] = self.gerar_imagem(img, cores)
            yield [tp.load_bar(len(nome_pecas), k+1)]

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[nome][cor]
