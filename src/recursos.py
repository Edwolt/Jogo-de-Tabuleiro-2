from pygame import image
from pygame import Color, Surface

import importlib


def Config(nome: str):
    return importlib.import_module(f'configs.{nome}').Config()


def caminho_asset(nome: str) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{nome}.png'


class Recursos:
    def __init__(self, config: str, size: tuple = (800, 800), framerate: int = 60):
        self.size = size
        self.framerate = framerate

        self.config = Config(config)
        self.assets = dict()

    def set_config(self, config: str) -> None:
        self.config = Config(config)

    def gerar_imagem(self, sprite: Surface, grad_preto: tuple, grad_branco: tuple) -> tuple:
        preto = sprite.copy()
        p1, p2 = grad_preto
        branco = sprite.copy()
        b1, b2 = grad_branco

        w, h = sprite.get_size()

        for i in range(w):
            for j in range(h):
                atual = sprite.get_at((i, j))
                np = Color(0, 0, 0, 0)
                nb = Color(0, 0, 0, 0)

                for k in range(len(atual)):
                    np[k] = int(p1[k] + (p2[k] - p1[k]) * (atual[k] / 255))
                    nb[k] = int(b1[k] + (b2[k] - b1[k]) * (atual[k] / 255))

                preto.set_at((i, j), np)
                branco.set_at((i, j), nb)

        return preto, branco

    def carregar(self):
        """Carrega os assets das peças na memória"""
        nome_pecas = ['rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao']
        yield [(len(nome_pecas), 0)]
        for k, i in enumerate(nome_pecas):
            self.assets[i] = self.gerar_imagem(
                image.load(caminho_asset(i)),
                (Color(0, 0, 0, 0), Color(100, 100, 100, 255)),
                (Color(100, 100, 100, 0), Color(255, 255, 255, 255))
            )
            yield [(len(nome_pecas), k+1)]

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[nome][1 if cor else 0]
