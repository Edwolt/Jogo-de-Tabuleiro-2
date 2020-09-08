import pygame


class Pecas():
    def __init__(self):
        self.assets = dict()
        self.pecas = ['Rei', 'Rainha', 'Bispo', 'Cavalo', 'Torre', 'Peao']

    def carregar(self):
        for i in pecas:
            nome_branco = f'assets/{i}_branco'
            nome_preto = f'assets/{i}_preto'

            self.assets.update({
                nome_branco: pygame.image.load(nome_branco),
                nome_preto: pygame.image.load(nome_preto)
            })

    def criar_peca(self, nome: str, cor: bool):
        if nome == 'Rei':
            return Rei(self.asset['Rei'], cor)
        elif nome == 'Rainha':
            return Rainha(self.asset['Rainha'], cor)
        elif nome == 'Bispo':
            return Bispo(self.asset['Bispo'], cor)
        elif nome == 'Cavalo':
            return Cavalo(self.asset['Cavalo'], cor)
        elif nome == 'Torre':
            return Torre(self.asset['Torre'], cor)
        elif nome == 'Peao':
            return Peao(self.asset['Peao'], cor)

    def load(self):
        pass


class Rei():
    def __init__(self, sprite: pygame.Surface, cor: bool):
        self.nome = 'Rei'
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
        self.sprite = sprite
        self.cor = cor
