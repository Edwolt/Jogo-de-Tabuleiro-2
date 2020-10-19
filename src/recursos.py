from pygame import image
from pygame import Color, Surface

import importlib


def Config(nome: str):
    return importlib.import_module(f'configs.{nome}').Config()


# TODO id e identificador não são bons nomes de variáveis
def id_peca(nome: str, cor: bool) -> str:
    """Retorna o identificador do tipo de peça"""
    return nome + ('1' if cor else '0')


def todos_ids() -> list:
    """Retorna uma lista com todos os identificadores de peças"""
    nome_pecas = ['rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao']
    return [(i, id_peca(i, False)) for i in nome_pecas] + [(i, id_peca(i, True)) for i in nome_pecas]


def caminho_asset(identificador: str) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{identificador}.png'


class Recursos:
    def __init__(self, config: str, size: tuple = (800, 800), framerate: int = 60):
        self.size = size
        self.framerate = framerate

        self.config = Config(config)
        self.assets = dict()

    def set_config(self, config: str) -> None:
        self.config = Config(config)

    def gerar_imagem(self, sprite: Surface, grad: tuple) -> Surface:
        res = sprite.copy()
        cor1, cor2 = grad

        w, h = res.get_size()

        from random import randint

        for i in range(w):
            for j in range(h):
                cor_atual = res.get_at((i, j))
                nova_cor = Color(0, 0, 0, 0)

                for k in range(len(nova_cor)):
                    novo = cor1[k] + (cor2[k] - cor1[k]) * (cor_atual[k] / 255)
                    nova_cor[k] = int(novo)

                res.set_at((i, j), nova_cor)

        return res

    def carregar(self):
        """Carrega os assets das peças em RAM"""
        identificadores = todos_ids()
        n = len(identificadores)

        yield [(n, 0)]
        for k, (nome, i) in enumerate(identificadores):
            self.assets[i] = self.gerar_imagem(
                image.load(caminho_asset(nome)),
                (Color(0, 0, 0, 0), Color(100, 0, 0, 255))
            )
            yield [(n, k+1)]

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[id_peca(nome, cor)]
