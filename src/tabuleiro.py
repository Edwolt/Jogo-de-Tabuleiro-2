from __future__ import annotations

from pygame import Surface

from types import SimpleNamespace
from typing import Optional

import tipos as tp
from recursos import Recursos
from pecas import Rei, Rainha, Bispo, Cavalo, Torre, Peao
from pecas import testar_xeque
from pecas import MovimentoEspecial


def novo_tabuleiro() -> tp.board:
    """
    Um tabuleiro com as peças na posição inicial
    :param pecas: objeto da classe Peca
    :return: matriz board onde os espacos vazios valem None
    e os espacos com pecas são objetos
    """

    # list 8x8 com None
    tabuleiro: tp.board = [
        [None] * 8 for _ in range(8)
    ]

    # Pretas
    tabuleiro[0][0] = Torre(False)
    tabuleiro[0][1] = Cavalo(False)
    tabuleiro[0][2] = Bispo(False)
    tabuleiro[0][3] = Rainha(False)
    tabuleiro[0][4] = Rei(False)
    tabuleiro[0][5] = Bispo(False)
    tabuleiro[0][6] = Cavalo(False)
    tabuleiro[0][7] = Torre(False)
    for i in range(8):  # Peões
        tabuleiro[1][i] = Peao(False)

    # Brancas
    tabuleiro[7][0] = Torre(True)
    tabuleiro[7][1] = Cavalo(True)
    tabuleiro[7][2] = Bispo(True)
    tabuleiro[7][3] = Rainha(True)
    tabuleiro[7][4] = Rei(True)
    tabuleiro[7][5] = Bispo(True)
    tabuleiro[7][6] = Cavalo(True)
    tabuleiro[7][7] = Torre(True)
    for i in range(8):  # Peões
        tabuleiro[6][i] = Peao(True)

    return tabuleiro


class Tabuleiro:
    def __init__(self):
        self.tabuleiro = novo_tabuleiro()
        self.vez = True
        self.flags = list()
        self.rei = tp.pb(tp.coord(0, 4), tp.coord(7, 4))

    def movimenta_peca(self, acao: tp.action, movimento: tp.movements) -> bool:
        """
        Movimenta a peça se o movimento for validao
        retornando se foi possível ou não

        :param pos: Posição da peça a ser movimentada
        :param nova_pos: Para onde será movimentada
        :return: Se a peça foi movimentada
        """

        (i, j), (m, n) = acao

        if isinstance(movimento, bool) and movimento:
            self.tabuleiro[m][n] = self.tabuleiro[i][j]
            self.tabuleiro[i][j] = None
            self.tabuleiro[m][n].notifica_movimento()

            if self.rei.branco == acao.pos:
                self.rei.branco = acao.nova_pos
            elif self.rei.preto == acao.pos:
                self.rei.preto = acao.nova_pos

            self.flags.clear()
            return True

        elif isinstance(movimento, MovimentoEspecial):
            movimento.executar(self.tabuleiro, self.flags)

            if movimento.nome == 'roque':
                if self.rei.branco == movimento.rei:
                    self.rei.branco = movimento.nova_rei
                elif self.rei.preto == movimento.rei:
                    self.rei.preto = movimento.nova_rei
            elif movimento.nome == 'promocao':
                self.promocao = movimento

            self.flags.clear()
            movimento.atualiza_flags(self.flags)
            return True

        return False

    def get_movimentos(self, pos: tp.coord) -> Optional[tp.movements]:
        """

        :param pos: [description]
        :return: Retorna um matriz movements com os movimentos legais para peça
        em pos
        Se pos não for uma peça aliada retorna None
        """

        i, j = pos
        peca = self.tabuleiro[i][j]
        if peca is None:
            return None
        elif peca.cor == self.vez:
            return peca.get_movimentos(
                self.tabuleiro,
                self.flags,
                self.rei[self.vez],
                pos
            )
        else:
            return None

    def draw(self, canvas: Surface, click: Optional[tp.coord], movimento: tp.movements) -> None:
        recursos = Recursos()

        size = canvas.get_size()
        size = size[0] // 8, size[1] // 8

        for y, linha in enumerate(self.tabuleiro):
            for x, peca in enumerate(linha):
                # i, j = y, x

                tipo = 'vazio'
                if click and tp.coord(y, x) == click:
                    tipo = 'click'
                elif movimento and movimento[y][x]:
                    if isinstance(movimento[y][x], MovimentoEspecial) and movimento[y][x].nome in ('roque', 'enpassant', 'avancoduplo'):
                        tipo = 'especial'
                    else:
                        tipo = 'movimento'
                elif ((y, x) == self.rei.branco or (y, x) == self.rei.preto) and testar_xeque(self.tabuleiro, self.flags, tp.coord(y, x)):
                    tipo = 'xeque'

                surf = Surface(size)
                recursos.config.quadrado(surf, tp.coord(x, y), tipo)

                if peca:
                    peca.draw(surf)

                pos = x * size[0], y * size[1]
                canvas.blit(surf, pos)
