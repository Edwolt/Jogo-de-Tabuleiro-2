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

        for i in range(w):
            for j in range(h):
                cor_atual = res.get_at((i, j))
                nova_cor = Color(
                    int(cor1.r + (cor2.r - cor1.r) * (cor_atual.r / 255)),
                    int(cor1.g + (cor2.g - cor1.g) * (cor_atual.g / 255)),
                    int(cor1.b + (cor2.b - cor1.b) * (cor_atual.b / 255)),
                    cor_atual.a
                )
                print(cor1, cor2, cor_atual, nova_cor)
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
                (Color(0, 0, 0), Color(100, 100, 100))
            )
            yield [(n, k)]
        yield [(n, n)]

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[id_peca(nome, cor)]
