import pygame
from pygame import Surface
from pygame import draw

from util import tabuleiro_false

# TODO transformar movimentos especiais em uma função ou um objeto em vez de uma tupla complexa

# TODO id e identificador não são bons nomes de variáveis


def id_peca(nome: str, cor: bool) -> str:
    """Retorna o identificador do tipo de peca"""
    identificador = nome
    identificador += '1' if cor else '0'
    return identificador


def caminho_asset(identificador: str) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{identificador}.png'


""" TODO
Ideia para fazer o movimento:
[ ] Encontra onde está o rei da mesma cor
[ ] Descobre quais pecas não podem sair do lugar por que criam xeque
[x] Calcula onde a peça em questão pode ir
[ ] Desconta do resultado onde as peças nao pode ir
"""


def protege_rei():
    # TODO verifica se movimentar para uma casa ataca o rei
    pass


def valida_coordenadas(a: int, b: int = 0) -> bool:
    """
    Verifica se uma coordanada é válida dentro do tabuleiro

    Pode ser usado das seguintes formas:
    * valida_coordenada(a)
      Verifica se o valor a é um valor válido para
      ser a componente de uma coordenada

    * valida_coordenada(a, b)
      Verifica se o valor da coordenada (a, b) é válido
    """
    return 0 <= a < 8 and 0 <= b < 8


def movimenta_direcao(res: list, tabuleiro: list, pos: tuple, direcao: tuple, cor: bool) -> None:
    di, dj = direcao
    i, j = pos

    i, j = i+di, j+dj
    while valida_coordenadas(i, j):
        if tabuleiro[i][j] is None:
            res[i][j] = True
        else:
            res[i][j] = cor != tabuleiro[i][j].cor
            break  # Se a casa não está vazia, não tem porquê olhar adiante
        i, j = i+di, j+dj


def calcula_direcao(res: list, tabuleiro: list, pos: tuple, direcoes: list, cor: bool) -> None:
    for direcao in direcoes:
        movimenta_direcao(res, tabuleiro, pos, direcao, cor)


class M():
    pass


class Roque(M):
    def __init__(self, pos_rei: tuple, pos_torre: tuple):
        self.nome = 'roque'

    def executar():
        pass


class P():
    """Classe abstrata para as peças"""

    # def __init__(self, sprite: Surface, cor: bool): pass

    def draw(self, canva) -> None:
        """Desenha o sprite na surface"""
        sprite_escala = pygame.transform.scale(self.sprite, canva.get_size())
        canva.blit(sprite_escala, (0, 0))

    def notifica_movimento(self):
        return

    # def get_movimentos(self, tabuleiro: list, pos: tuple) -> list: pass


class Rei(P):
    def __init__(self, sprite: Surface, cor: bool, movimentou: bool = False):
        """
        :param sprite: Uma Surface com a imagem da peca
        :param cor: True: 'branco'; False: 'preto'
        """

        self.nome = 'rei'
        self.sprite = sprite
        self.cor = cor

        self.movimentou = movimentou

    def notifica_movimento(self):
        self.movimentou = True

    def valida_posicao(self, tabuleiro: list, pos: tuple) -> bool:
        i, j = pos
        return tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        """
        :return: list 8x8 dizendo se é possivel movimentar ou não
        Caso seja um tuple é porque o movimento é especial, onde:
        * O primeiro elemento o nome do movimento
        * Os próximos elementos são tuples com as coordenadas e o que ela deve receber
        """
        # TODO Cuidado com cheque

        res = tabuleiro_false()
        i, j = pos

        # Casas acima do rei
        if valida_coordenadas(i-1, j-1):
            res[i-1][j-1] = self.valida_posicao(tabuleiro, (i-1, j-1))
        if valida_coordenadas(i-1, j):
            res[i-1][j] = self.valida_posicao(tabuleiro, (i-1, j))
        if valida_coordenadas(i-1, j + 1):
            res[i-1][j+1] = self.valida_posicao(tabuleiro, (i-1, j+1))

        # Casas do meio
        if valida_coordenadas(i, j-1):
            res[i][j-1] = self.valida_posicao(tabuleiro, (i, j-1))
        if valida_coordenadas(i-1, j+1):
            res[i][j+1] = self.valida_posicao(tabuleiro, (i, j+1))

        # Casas abaixo do rei
        if valida_coordenadas(i+1, j-1):
            res[i+1][j-1] = self.valida_posicao(tabuleiro, (i, j-1))
        if valida_coordenadas(i+1, j):
            res[i+1][j] = self.valida_posicao(tabuleiro, (i+1, j))
        if valida_coordenadas(i+1, j-1):
            res[i+1][j-1] = self.valida_posicao(tabuleiro, (i+1, j-1))

        # Verifica se é possível fazer o Roque
        if not self.movimentou:
            torre = tabuleiro[i][0]
            if torre is not None and torre.nome == 'torre' and not torre.movimentou:
                # TODO verifica se deixa o rei em xeque ou passa em casas em xeque

                pecas_entre = False
                for jj in range(1, j):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                if not pecas_entre:
                    res[i][j-2] = (
                        'roque',
                        ((i, j-2), self),
                        ((i, j-1), torre),
                        ((i, j), None),
                        ((i, 0), None),
                    )

            torre = tabuleiro[i][7]
            if torre is not None and torre.nome == 'torre' and not torre.movimentou:
                pecas_entre = False
                for jj in range(j + 1, 7):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                if not pecas_entre:
                    res[i][j-2] = (
                        'roque',
                        ((i, j+2), self),
                        ((i, j+1), torre),
                        ((i, j), None),
                        ((i, 7), None),
                    )

        return res


class Rainha(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'rainha'
        self.sprite = sprite
        self.cor = cor

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        res = tabuleiro_false()
        direcoes = (
            (-1, 0),   # Cima
            (1, 0),    # Baixo
            (0, -1),   # Esquerda
            (0, 1),    # Direita
            (-1, 1),   # Cima Direita
            (-1, -1),  # Cima Esquerda
            (1, 1),    # Baixo Direita
            (1, -1),   # Baixo Esquerda
        )

        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res


class Bispo(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'bispo'
        self.sprite = sprite
        self.cor = cor

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        res = tabuleiro_false()
        direcoes = (
            (-1, 1),   # Cima Direita
            (-1, -1),  # Cima Esquerda
            (1, 1),    # Baixo Direita
            (1, -1),   # Baixo Esquerda
        )

        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res


class Cavalo(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'cavalo'
        self.sprite = sprite
        self.cor = cor

    def valida_posicao(self, tabuleiro: list, pos: tuple) -> bool:
        i, j = pos
        return tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        res = tabuleiro_false()
        i, j = pos

        # Casas acima
        if valida_coordenadas(i-2, j-1):
            res[i-2][j-1] = self.valida_posicao(tabuleiro, (i-2, j-1))
        if valida_coordenadas(i-2, j+1):
            res[i-2][j+1] = self.valida_posicao(tabuleiro, (i-2, j+1))

        # Casas abaixo
        if valida_coordenadas(i+2, j-1):
            res[i+2][j-1] = self.valida_posicao(tabuleiro, (i+2, j-1))
        if valida_coordenadas(i+2, j+1):
            res[i+2][j+1] = self.valida_posicao(tabuleiro, (i+2, j+1))

        # Casas a esquerda
        if valida_coordenadas(i-1, j-2):
            res[i-1][j-2] = self.valida_posicao(tabuleiro, (i-1, j-2))
        if valida_coordenadas(i+1, j-2):
            res[i+1][j-2] = self.valida_posicao(tabuleiro, (i+1, j-2))

        # Casas a direira
        if valida_coordenadas(i-1, j+2):
            res[i-1][j+2] = self.valida_posicao(tabuleiro, (i-1, j+2))
        if valida_coordenadas(i+1, j+2):
            res[i+1][j+2] = self.valida_posicao(tabuleiro, (i+1, j+2))

        return res


class Torre(P):
    def __init__(self, sprite: Surface, cor: bool, movimentou: bool = False):
        self.nome = 'torre'
        self.sprite = sprite
        self.cor = cor

        self.movimentou = movimentou

    def notifica_movimento(self):
        self.movimentou = True

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        res = tabuleiro_false()
        direcoes = (
            (-1, 0),  # Cima
            (1, 0),   # Baixo
            (0, -1),  # Esquerda
            (0, 1),   # Direita
        )

        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)

        return res


class Peao(P):
    def __init__(self, sprite: Surface, cor: bool, movimentou: bool = False):
        self.nome = 'peao'
        self.sprite = sprite
        self.cor = cor
        self.movimentou = movimentou

    def notifica_movimento(self):
        self.movimentou = True

    def criar_captura(self, tabuleiro: list, pos: tuple, nova_pos: tuple):
        m, n = pos
        i, j = nova_pos
        promocao = 0 if self.cor else 7

        if tabuleiro[i][j] is not None and tabuleiro[i][j].cor != self.cor:
            # TODO enpassant
            if i == promocao:
                return 'promocao'
            else:
                return True
        else:
            return False

    def get_movimentos(self, tabuleiro: list, pos: tuple) -> list:
        # TODO Promoção

        res = tabuleiro_false()
        promocao = 0 if self.cor else 7

        i, j = pos
        i += -1 if self.cor else 1
        if valida_coordenadas(i) and tabuleiro[i][j] is None:
            res[i][j] = 'promocao' if i == promocao else True
            i += -1 if self.cor else 1
            if not self.movimentou and valida_coordenadas(i) and tabuleiro[i][j] is None:
                res[i][j] = 'promocao' if i == promocao else True  # TODO enpassant

        i, j = pos
        i += -1 if self.cor else 1
        if valida_coordenadas(i, j-1):
            res[i][j-1] = self.criar_captura(tabuleiro, pos, (i, j-1))
        if valida_coordenadas(i, j+1):
            res[i][j+1] = self.criar_captura(tabuleiro, pos, (i, j+1))

        return res


class Pecas():
    """Ajuda na criação de objetos pecas"""

    def __init__(self):
        self.assets = dict()

    def carregar(self) -> None:
        """Carrega os assets das peças em RAM"""

        pecas = ['rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao']
        for i in pecas:
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
        return Rei(self.get_asset('rei', cor), cor, movimentou=movimentou)

    def Rainha(self, cor: bool) -> Rainha:
        return Rainha(self.get_asset('rainha', cor), cor)

    def Bispo(self, cor: bool) -> Bispo:
        return Bispo(self.get_asset('bispo', cor), cor)

    def Cavalo(self, cor: bool) -> Cavalo:
        return Cavalo(self.get_asset('cavalo', cor), cor)

    def Torre(self, cor: bool, movimentou: bool = False) -> Torre:
        return Torre(self.get_asset('torre', cor), cor, movimentou=movimentou)

    def Peao(self, cor: bool, movimentou: bool = False) -> Peao:
        return Peao(self.get_asset('peao', cor), cor, movimentou=movimentou)
