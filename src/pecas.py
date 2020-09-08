import pygame


# TODO id e identificador não são bons nomes de variáveis para esse contexto
def id_peca(nome: str, cor: bool) -> str:
    """Retorna o identificador do tipo de peca"""

    cor_str = 'branco' if cor else 'preto'
    return f'{nome}_{cor_str}'


def caminho_asset(identificador: str) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""

    return f'assets/{identificador}.png'


def draw_image(canva, sprite) -> None:
    """Desenha sprite em canva"""

    sprite = pygame.transform.scale(sprite, canva.get_size())
    canva.blit(sprite, (0, 0))


class Rei():
    def __init__(self, sprite, cor: bool):
        """
        :param sprite: Uma Surface com a imagem da peca
        :param cor: True: 'branco'; False: 'preto'
        """

        self.nome = 'Rei'
        self.identificador = id_peca(self.nome, cor)
        self.sprite = sprite
        self.cor = cor

    def draw(self, canva):
        """Desenha o sprite em canva"""
        draw_image(canva, self.sprite)


class Rainha():
    def __init__(self, sprite, cor: bool):
        self.nome = 'Rainha'
        self.sprite = sprite
        self.cor = cor

    def draw(self, canva):
        draw_image(canva, self.sprite)


class Bispo():
    def __init__(self, sprite, cor: bool):
        self.nome = 'Bispo'
        self.sprite = sprite
        self.cor = cor

    def draw(self, canva):
        draw_image(canva, self.sprite)


class Cavalo():
    def __init__(self, sprite, cor: bool):
        self.nome = 'Cavalo'
        self.sprite = sprite
        self.cor = cor

    def draw(self, canva):
        draw_image(canva, self.sprite)


class Torre():
    def __init__(self, sprite, cor: bool):
        self.nome = 'Torre'
        self.sprite = sprite
        self.cor = cor

    def draw(self, canva):
        draw_image(canva, self.sprite)


class Peao():
    def __init__(self, sprite, cor: bool):
        self.nome = 'Peao'
        self.identificador = id_peca(self.nome, cor)
        self.sprite = sprite
        self.cor = cor

    def draw(self, canva):
        draw_image(canva, self.sprite)


class Pecas():
    def __init__(self):
        self.assets = dict()
        self.pecas = ['Rei', 'Rainha', 'Bispo', 'Cavalo', 'Torre', 'Peao']

    def carregar(self) -> None:
        """Carrega os assets das peças em RAM"""

        for i in self.pecas:
            id_branco = id_peca(i, True)
            id_preto = id_peca(i, False)

            self.assets.update({
                id_branco: pygame.image.load(caminho_asset(id_branco)),
                id_preto: pygame.image.load(caminho_asset(id_preto))
            })

    def get_asset(self, nome: str, cor: bool) -> pygame.Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[id_peca(nome, cor)]

    def Rei(self, cor: bool):
        return Rei(self.get_asset('Rei', cor), cor)

    def Rainha(self, cor: bool):
        return Rainha(self.get_asset('Rainha', cor), cor)

    def Bispo(self, cor: bool):
        return Bispo(self.get_asset('Bispo', cor), cor)

    def Cavalo(self, cor: bool):
        return Cavalo(self.get_asset('Cavalo', cor), cor)

    def Torre(self, cor: bool):
        return Torre(self.get_asset('Torre', cor), cor)

    def Peao(self, cor: bool):
        return Peao(self.get_asset('Peao', cor), cor)
