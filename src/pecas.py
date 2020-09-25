import pygame
from pygame import draw, transform, image
from pygame import Surface

from util import tabuleiro_false


""" TODO
Ideia para fazer o movimento:
[ ] Encontra onde está o rei da mesma cor
[ ] Descobre quais pecas não podem sair do lugar por que criam xeque
[x] Calcula onde a peça em questão pode ir
[ ] Desconta do resultado onde as peças nao pode ir
"""


##### Movimentos #####
def mover_peca(tabuleiro: list, pos: tuple, nova_pos: tuple) -> None:
    i, j = pos
    m, n = nova_pos
    tabuleiro[m][n] = tabuleiro[i][j]
    tabuleiro[m][n].notifica_movimento()
    tabuleiro[i][j] = None


class M():
    """Classe abstrata para os movimentos especiais"""

    def executar(self, tabuleiro: list, pecas, flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """
        pass

    def update_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        pass


class Roque(M):
    def __init__(self, rei: tuple, nova_rei: tuple, torre: tuple, nova_torre):
        """[summary]
        :param rei: posição atual do rei
        :param nova_rei: posiçãol para a qual o rei será movido
        :param torre: posição atual da torre
        :param nova_torre: posição para o qual a torre será movida
        """

        self.nome = 'roque'
        self.rei = rei
        self.nova_rei = nova_rei
        self.torre = torre
        self.nova_torre = nova_torre

    def executar(self, tabuleiro: list, flags: list, pecas) -> None:
        mover_peca(tabuleiro, self.rei, self.nova_rei)
        mover_peca(tabuleiro, self.torre, self.nova_torre)


class Promocao(M):
    def __init__(self, pos: tuple, promocao: tuple):
        """
        :param pos: posição atual do peão
        :param promocao: posição para o qual o peão será movido causando a promoção
        """

        self.nome = 'promocao'
        self.pos = pos
        self.promocao = promocao
        pass

    def executar(self, tabuleiro: list, flags: list, pecas) -> None:
        i, j = self.pos
        cor = tabuleiro[i][j].cor
        tabuleiro[i][j] = None

        i, j = self.promocao
        tabuleiro[i][j] = pecas.Rainha(cor)


class AvancoDuplo(M):
    def __init__(self, cor: bool, pos: tuple, meio: tuple, nova_pos: tuple):
        """
        :param cor: cor da peça (True: 'branco'; False: 'preto')
        :param pos: posicão do peão
        :param meio: posição pela qual o peão passará
        :param nova_pos: posição final do peão
        """

        self.cor = cor
        self.pos = pos
        self.meio = meio
        self.nova_pos = nova_pos

    def executar(self, tabuleiro: list, flags: list, pecas) -> None:
        mover_peca(tabuleiro, self.pos, self.nova_pos)

    def update_flags(self, flags: list) -> None:
        flags.append(
            (
                'enpassant',
                self.cor,
                self.meio,
                self.nova_pos
            )
        )


class EnPassant(M):
    def __init__(self, pos: tuple, capturado_pos: tuple, nova_pos: tuple):
        """
        :param pos: posição do peão aliado
        :param capturado_pos: posição do peão inimigo a ser capturado
        :param nova_pos: posição para o qual o peão aliado será movido
        """

        self.nome = 'enpassant'
        self.pos = pos
        self.capturado_pos = capturado_pos
        self.nova_pos = nova_pos

    def executar(self, tabuleiro: list, flags: list, pecas) -> None:
        mover_peca(tabuleiro, self.pos, self.nova_pos)
        i, j = self.capturado_pos
        tabuleiro[i][j] = None


##### Peças #####
def valida_coordenadas(a: int, b: int = 0) -> bool:
    """
    valida_coordenada(a):    Verifica se a é um valor válido para componente de uma coordenada
    valida_coordenada(a, b): Verifica se (a, b) é uma coordenada válida
    """
    return 0 <= a < 8 and 0 <= b < 8


def calcula_direcao(res: list, tabuleiro: list, pos: tuple, direcoes: list, cor: bool) -> None:
    for (di, dj) in direcoes:
        i, j = pos
        i, j = i + di, j + dj
        while valida_coordenadas(i, j):
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = cor != tabuleiro[i][j].cor
                break  # Se a casa não está vazia, não tem porquê olhar adiante
            i, j = i + di, j + dj


class P():
    """Classe abstrata para as peças"""

    def __init__(self, sprite: Surface, cor: bool):
        """
        :param sprite: Uma Surface com a imagem da peca
        :param cor: True: 'branco'; False: 'preto'
        """
        pass

    def draw(self, canva) -> None:
        """Desenha o sprite na surface"""
        sprite_escala = transform.scale(self.sprite, canva.get_size())
        canva.blit(sprite_escala, (0, 0))

    def notifica_movimento(self) -> None:
        return

    def get_movimentos(self, tabuleiro: list, flags: list, pos: tuple) -> list:
        """
        :param flags: flags do tabuleiro
        :return: list 8x8 dizendo se é possivel movimentar ou não
        Caso o movimento seja especial é retornado um objeto de uma subclasse de M
        """
        pass


class Rei(P):
    def __init__(self, sprite: Surface, cor: bool, movimentou: bool = False):
        self.nome = 'rei'
        self.sprite = sprite
        self.cor = cor

        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def valida_posicao(self, tabuleiro: list, pos: tuple) -> bool:
        i, j = pos
        return tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

    def get_movimentos(self, tabuleiro: list, flags: list, pos: tuple) -> list:
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
                    res[i][j-2] = Roque((i, j), (i, j-2), (i, 0), (i, j-1))

            torre = tabuleiro[i][7]
            if torre is not None and torre.nome == 'torre' and not torre.movimentou:
                pecas_entre = False
                for jj in range(j + 1, 7):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                if not pecas_entre:
                    res[i][j+2] = Roque((i, j), (i, j+2), (i, 7), (i, j+1))

        return res


class Rainha(P):
    def __init__(self, sprite: Surface, cor: bool):
        self.nome = 'rainha'
        self.sprite = sprite
        self.cor = cor

    def get_movimentos(self, tabuleiro: list, flags: list, pos: tuple) -> list:
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

    def get_movimentos(self, tabuleiro: list, flags: list, pos: tuple) -> list:
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

    def get_movimentos(self, tabuleiro: list, flags: list, pos: tuple) -> list:
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

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def get_movimentos(self, tabuleiro: list, flags: list, pos: tuple) -> list:
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

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def get_enpassant(self, flags: list, nova_pos):
        for flag in flags:
            if flag[0] == 'enpassant':
                _, cor, meio, final = flag
                if self.cor != cor and nova_pos == meio:
                    return meio, final
        return None

    def criar_captura(self, tabuleiro: list, flags: list, pos: tuple, nova_pos: tuple):
        m, n = pos
        i, j = nova_pos
        promocao = 0 if self.cor else 7

        if tabuleiro[i][j] is not None and tabuleiro[i][j].cor != self.cor:
            # TODO enpassant
            if i == promocao:
                return Promocao(pos, nova_pos)
            else:
                return True
        else:
            enpassant = self.get_enpassant(flags, nova_pos)
            if enpassant is not None:
                meio, final = enpassant
                return EnPassant(pos, final, meio)
            else:
                return False

    def get_movimentos(self, tabuleiro: list, flags: list, pos: tuple) -> list:
        res = tabuleiro_false()
        promocao = 0 if self.cor else 7

        i, j = pos
        i += -1 if self.cor else 1
        if valida_coordenadas(i) and tabuleiro[i][j] is None:
            res[i][j] = Promocao(pos, (i, j)) if i == promocao else True
            ii = i-1 if self.cor else i+1
            if not self.movimentou and valida_coordenadas(ii) and tabuleiro[ii][j] is None:
                if i == promocao:
                    res[ii][j] = Promocao(pos, (ii, j))
                else:
                    res[ii][j] = AvancoDuplo(self.cor, pos, (i, j), (ii, j))

        i, j = pos
        i += -1 if self.cor else 1
        if valida_coordenadas(i, j-1):
            res[i][j-1] = self.criar_captura(tabuleiro, flags, pos, (i, j-1))
        if valida_coordenadas(i, j+1):
            res[i][j+1] = self.criar_captura(tabuleiro, flags, pos, (i, j+1))

        return res


##### Exportando Peças #####
# TODO id e identificador não são bons nomes de variáveis
def id_peca(nome: str, cor: bool) -> str:
    """Retorna o identificador do tipo de peca"""
    identificador = nome
    identificador += '1' if cor else '0'
    return identificador


def caminho_asset(identificador: str) -> str:
    """Retorna o caminho para o asset da peca com o identificador passado"""
    return f'assets/{identificador}.png'


class Pecas():
    """Ajuda na criação de objetos pecas"""

    def __init__(self):
        self.assets = dict()

    def carregar(self) -> None:
        """Carrega os assets das peças em RAM"""

        for i in ['rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao']:
            id_branco = id_peca(i, True)
            id_preto = id_peca(i, False)

            self.assets.update({
                id_branco: image.load(caminho_asset(id_branco)),
                id_preto: image.load(caminho_asset(id_preto))
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
