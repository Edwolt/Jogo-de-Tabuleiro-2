from pygame import image
from pygame import Surface

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
    return [id_peca(i, False) for i in nome_pecas] + [id_peca(i, True) for i in nome_pecas]


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

    def carregar(self):
        """Carrega os assets das peças em RAM"""
        identificadores = todos_ids()
        n = len(identificadores)

        yield [(n, 0)]
        for k, i in enumerate(identificadores):
            self.assets[i] = image.load(caminho_asset(i))
            yield [(n, k)]

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[id_peca(nome, cor)]
