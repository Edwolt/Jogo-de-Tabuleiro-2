import pygame
from pygame import Surface

from util import tabuleiro_false


# TODO id e identificador não são bons nomes de variáveis para esse contexto
def id_peca(nome: str, cor: bool) -> str:
    """Retorna o identificador do tipo de peca"""
    cor_str = 'branco' if cor else 'preto'
    return f'{nome}_{cor_str}'


def caminho_asset(identificador: str) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{identificador}.png'


''' TODO
Ideia para fazer o movimento:
* Encontra onde está o rei da mesma cor
* Descobre quais pecas não podem sair do lugar por que criam xeque
* Calcula onde a peça em questão pode ir
* Desconta do resultado onde as peças nao pode ir
'''


def protege_rei():
    # TODO verifica se movimentar para uma casa ataca o rei
    pass


def valida_coordenadas(a, b=0):
    return 0 <= a < 8 and 0 <= b < 8


def valida_posicao(tabuleiro, pos, cor):
    linha, coluna = pos
    return tabuleiro[linha][coluna] is None or tabuleiro[linha][coluna].cor != cor


class P():
    """Classe abstrata para as peças"""

    def draw(self, canva) -> None:
        """Desenha o sprite na surface"""
        sprite_escala = pygame.transform.scale(self.sprite, canva.get_size())
        canva.blit(sprite_escala, (0, 0))


class Rei(P):
    def __init__(self, sprite: Surface, cor: bool, movimentou: bool = False):
        """
        :param sprite: Uma Surface com a imagem da peca
        :param cor: True: 'branco'; False: 'preto'
        """

        self.nome = 'Rei'
        self.sprite = sprite
        self.cor = cor
        self.movimentou = movimentou

    def valida_movimento(self, tabuleiro: list, old_pos: tuple, new_pos: tuple) -> bool:
        # TODO Cuidado com cheque
        # TODO Roque
        pass

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        # TODO Cuidado com cheque
        # TODO Roque

        i, j = pos

        res = tabuleiro_false()

        # Casas acima do rei
        if(valida_coordenadas(i-1, j-1)):
            res[i-1][j-1] = valida_posicao(tabuleiro, (i-1, j-1), self.cor)

        if(valida_coordenadas(i-1, j)):
            res[i-1, j] = valida_posicao(tabuleiro, (i-1, j), self.cor)

        if(valida_coordenadas(i-1, j + 1)):
            res[i-1, j+1] = valida_posicao(tabuleiro, (i-1, j+1), self.cor)

        # Casas do meio
        if(valida_coordenadas(i, j-1)):
            res[i, j-1] = valida_posicao(tabuleiro, (i, j-1), self.cor)

        if(valida_coordenadas(i-1, j+1)):
            res[i, j+1] = valida_posicao(tabuleiro, (i, j+1), self.cor)

        # Casas abaixo do rei
        if(valida_coordenadas(i+1, j-1)):
            res[i+1, j-1] = valida_posicao(tabuleiro, (i, j-1), self.cor)

        if(valida_coordenadas(i+1, j)):
            res[i+1, j] = valida_posicao(tabuleiro, (i+1, j), self.cor)

        if(valida_coordenadas(i+1, j-1)):
            res[i+1, j-1] = valida_posicao(tabuleiro, (i+1, j-1), self.cor)


class Rainha(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'Rainha'
        self.sprite = sprite
        self.cor = cor

    def valida_movimento(self, tabuleiro: list, old_pos: tuple, new_pos: tuple) -> bool:
        # TODO
        pass

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        # TODO
        pass


class Bispo(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'Bispo'
        self.sprite = sprite
        self.cor = cor

    def valida_movimento(self, tabuleiro: list, old_pos: tuple, new_pos: tuple) -> bool:
        # TODO
        pass

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        # TODO
        pass


class Cavalo(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'Cavalo'
        self.sprite = sprite
        self.cor = cor

    def valida_movimento(self, tabuleiro: list, old_pos: tuple, new_pos: tuple) -> bool:
        # TODO
        pass

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        # TODO
        pass


class Torre(P):
    def __init__(self, sprite: Surface, cor: bool, movimentou: bool = False):
        self.nome = 'Torre'
        self.sprite = sprite
        self.cor = cor

    def valida_movimento(self, tabuleiro: list, old_pos: tuple, new_pos: tuple) -> bool:
        # TODO Roque
        pass

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        # TODO Roque
        pass


class Peao(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'Peao'
        self.identificador = id_peca(self.nome, cor)
        self.sprite = sprite
        self.cor = cor

    def valida_movimento(self, tabuleiro: list, old_pos: tuple, new_pos: tuple) -> bool:
        # TODO Promoção
        # TODO EnPassant
        pass

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        # TODO Promoção
        # TODO EnPassant
        pass


class Pecas():
    """Ajuda na criação de objetos pecas"""

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

    def get_asset(self, nome: str, cor: bool) -> Surface:
        """Retorna o asset da peca com o nome e a cor dada"""
        return self.assets[id_peca(nome, cor)]

    def Rei(self, cor: bool, movimentou: bool = False) -> Rei:
        return Rei(self.get_asset('Rei', cor), cor, movimentou=movimentou)

    def Rainha(self, cor: bool) -> Rainha:
        return Rainha(self.get_asset('Rainha', cor), cor)

    def Bispo(self, cor: bool) -> Bispo:
        return Bispo(self.get_asset('Bispo', cor), cor)

    def Cavalo(self, cor: bool) -> Cavalo:
        return Cavalo(self.get_asset('Cavalo', cor), cor)

    def Torre(self, cor: bool, movimentou: bool = False) -> Torre:
        return Torre(self.get_asset('Torre', cor), cor, movimentou=movimentou)

    def Peao(self, cor: bool) -> Peao:
        return Peao(self.get_asset('Peao', cor), cor)
