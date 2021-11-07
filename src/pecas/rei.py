from recursos import Recursos
from tipos import board, movements, coord, action

from .abc_peca import Peca
from .abc_movimento import MovimentoEspecial
from .xeque import testar_xeque
from .util import tabuleiro_false, tabuleiro_copia, mover_peca


class Roque(MovimentoEspecial):
    def __init__(self, acao_rei: action, acao_torre: action):
        """
        :param rei: posição atual do rei
        :param nova_rei: posição para a qual o rei será movido
        :param torre: posição atual da torre
        :param nova_torre: posição para o qual a torre será movida
        """

        super().__init__(nome='roque')
        self.acao_rei = acao_rei
        self.acao_torre = acao_torre

    def executar(self, tabuleiro: board, flags: list) -> None:
        mover_peca(tabuleiro, self.acao_rei)
        mover_peca(tabuleiro, self.acao_torre)


class Rei(Peca):
    def __init__(self, cor: bool, movimentou: bool = False):
        super().__init__(cor, nome='rei')
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def valida_posicao(self, tabuleiro: board, pos: coord) -> bool:
        i, j = pos
        return tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

    def get_movimentos_simples(self, tabuleiro: board, flags: list, pos: coord) -> movements:
        # TODO Cuidado com cheque
        res = tabuleiro_false()
        i, j = pos

        # Casas acima do rei
        if coord(i-1, j-1).valida:
            res[i-1][j-1] = self.valida_posicao(tabuleiro, coord(i-1, j-1))
        if coord(i-1, j).valida:
            res[i-1][j] = self.valida_posicao(tabuleiro, coord(i-1, j))
        if coord(i-1, j+1).valida():
            res[i-1][j+1] = self.valida_posicao(tabuleiro, coord(i-1, j+1))

        # Casas do meio
        if coord(i, j-1).valida:
            res[i][j-1] = self.valida_posicao(tabuleiro, coord(i, j-1))
        if coord(i, j+1).valida:
            res[i][j+1] = self.valida_posicao(tabuleiro, coord(i, j+1))

        # Casas abaixo do rei
        if coord(i+1, j-1).valida():
            res[i+1][j-1] = self.valida_posicao(tabuleiro, coord(i+1, j-1))
        if coord(i+1, j).valida():
            res[i+1][j] = self.valida_posicao(tabuleiro, coord(i+1, j))
        if coord(i+1, j+1).valida():
            res[i+1][j+1] = self.valida_posicao(tabuleiro, coord(i+1, j+1))

        # Verifica se é possível fazer o Roque
        if not self.movimentou:
            torre = tabuleiro[i][0]
            if torre is not None and torre.nome == 'torre' and not torre.movimentou:
                # TODO verifica se deixa o rei em xeque ou passa em casas em xeque

                pecas_entre = False
                for jj in range(1, j):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                tab = tabuleiro_copia(tabuleiro)
                tab[i][3] = Rei(self.cor)
                tab[i][4] = None
                xeque = testar_xeque(tab, flags, coord(i, 3))

                if not xeque:
                    tab = tabuleiro_copia(tabuleiro)
                    tab[i][2] = Rei(self.cor)
                    tab[i][4] = None
                    xeque = testar_xeque(tab, flags, coord(i, 2))

                if not pecas_entre and not xeque:
                    res[i][j-2] = Roque(
                        action(coord(i, j), coord(i, j-2)),
                        action(coord(i, 0), coord(i, j-1))
                    )

            torre = tabuleiro[i][7]
            if torre is not None and torre.nome == 'torre' and not torre.movimentou:
                pecas_entre = False
                for jj in range(j + 1, 7):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                if not pecas_entre:
                    res[i][j+2] = Roque(
                        action(coord(i, j), coord(i, j+2)),
                        action(coord(i, 7), coord(i, j+1))
                    )

        return res
