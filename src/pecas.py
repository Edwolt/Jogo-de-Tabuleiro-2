import pygame


def id_peca(nome: str, cor: bool) -> str:
    cor_str = 'braco' if cor else 'preto'
    return f'{nome}_{cor_str}'


def caminho_asset(identificador: str) -> str:
    return f'assets/{identificador}'


class Pecas():
    def __init__(self):
        self.assets = dict()
        self.pecas = ['Rei', 'Rainha', 'Bispo', 'Cavalo', 'Torre', 'Peao']

    def carregar(self) -> None:
        for i in pecas:
            id_branco = id_peca(i, True)
            id_preto = id_peca(i, False)

            self.assets.update({
                id_branco: pygame.image.load(caminho_asset(id_branco)),
                id_preto: pygame.image.load(caminho_asset(id_preto))
            })

    def criar_peca(self, nome: str, cor: bool):
        sprite = self.assets[id_peca(nome, cor)]
        if nome == 'Rei':
            return Rei(sprite, cor)
        elif nome == 'Rainha':
            return Rainha(sprite, cor)
        elif nome == 'Bispo':
            return Bispo(sprite, cor)
        elif nome == 'Cavalo':
            return Cavalo(sprite, cor)
        elif nome == 'Torre':
            return Torre(sprite, cor)
        elif nome == 'Peao':
            return Peao(sprite, cor)


class Rei():
    def __init__(self, sprite: pygame.Surface, cor: bool):
        self.nome = 'Rei'
        self.identificador = id_peca(self.nome, cor)
        self.sprite = sprite
        self.cor = cor


class Rainha():
    def __init__(self, sprite: pygame.Surface, cor: bool):
        self.nome = 'Rainha'
        self.sprite = sprite
        self.cor = cor


class Bispo():
    def __init__(self, sprite: pygame.Surface, cor: bool):
        self.nome = 'Bispo'
        self.sprite = sprite
        self.cor = cor


class Cavalo():
    def __init__(self, sprite: pygame.Surface, cor: bool):
        self.nome = 'Cavalo'
        self.sprite = sprite
        self.cor = cor


class Torre():
    def __init__(self, sprite: pygame.Surface, cor: bool):
        self.nome = 'Torre'
        self.sprite = sprite
        self.cor = cor


class Peao():
    def __init__(self, sprite: pygame.Surface, cor: bool):
        self.nome = 'Peao'
        self.identificador = id_peca(self.nome, cor)
        self.sprite = sprite
        self.cor = cor
