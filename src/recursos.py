from __future__ import annotations

import pygame as pg
import importlib

import tipos as tp
from abc_config import Config
from singleton import Singleton
from pecas import LISTA_NOME_PECAS


def get_config(nome: str) -> Config:
    module = importlib.import_module(f'configs.{nome.lower()}')
    cls = getattr(module, 'export')
    return cls()


def caminho_asset(nome: str, png_min: bool = False) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{nome}.png' + ('.min' if png_min else '')


class Recursos(metaclass=Singleton):
    def __init__(
        self,
        size: tuple[int, int] = (800, 800),
        framerate: int = 60,
        png_min: bool = False
    ):
        self.size = size
        self.framerate = framerate
        self._png_min = png_min

        self._config = None
        self._assets = dict()

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

    def gerar_imagem(
        self,
        sprite: pg.Surface,
        gradientes: tp.pb[tp.grad]
    ) -> tp.pb[pg.Surface]:
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
                sprites.preto.set_at((i, j), gradientes.preto.gerar_cor(cor))
                sprites.branco.set_at((i, j), gradientes.branco.gerar_cor(cor))

        return sprites

    def carregar(self) -> tp.load_gen:
        """Carrega os assets das peças na memória"""
        cores = self.config.pecas_cor()
        yield [tp.load_bar(len(LISTA_NOME_PECAS), 0)]
        for k, i in enumerate(LISTA_NOME_PECAS):
            try:
                img = pg.image.load(caminho_asset(i, self._png_min))
            except:
                img = pg.image.load(caminho_asset(i))

            self._assets[i] = self.gerar_imagem(img, cores)
            yield [tp.load_bar(len(LISTA_NOME_PECAS), k+1)]

    def get_asset(self, nome: str, cor: bool) -> pg.Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self._assets[nome][cor]
