from __future__ import annotations

import tipos as tp

from .abc_peca import Peca
from .abc_movimento import Movimento, MovimentoComplexo
from .util import movements_vazio, mover_peca


class Promocao(MovimentoComplexo):
    especial: bool = True

    def __init__(self, acao: tp. action, cor: bool):
        """
        :param pos: posição atual do peão
        :param cor: cor da peça (False: 'preto'; True: 'branco')
        """
        self.pos = acao.pos
        self.promocao = acao.nova_pos
        self.cor = cor
        pass

    def executar(self, tabuleiro: tp.board, flags: list) -> None:
        i, j = self.pos
        m, n = self.promocao
        tabuleiro[m][n] = tabuleiro[i][j]
        tabuleiro[i][j] = None

        peca = tabuleiro[m][n]
        peca is None or peca.notifica_movimento()


class Avanco(MovimentoComplexo):
    avanco: bool = True

    def __init__(self, cor: bool, pos: tp.coord):
        self.cor = cor
        self.pos = pos

    def executar(self, tabuleiro: tp.board, flags: list):
        i, j = self.pos
        i += -1 if self.cor else 1
        mover_peca(tabuleiro, tp.action(self.pos, tp.coord(i, j)))


class AvancoDuplo(MovimentoComplexo):
    avanco: bool = True
    especial: bool = True

    def __init__(self, cor: bool, caminho_acao: tp.pathaction):
        """
        :param cor: cor da peça (False: 'preto', True: 'branco'; )
        :param pathaction: movimento que o peão fará
        * pos: posição do peão
        * meio: posição pela qual o peão passará para que seja possível calcular onde ele poderá ser capturado por enpassant
        * nova_pos: posição final do peão
        """
        self.cor = cor
        self.caminho_acao = caminho_acao

    def executar(self, tabuleiro: tp.board, flags: list) -> None:
        mover_peca(tabuleiro, self.caminho_acao.to_action())

    def update_flags(self, flags: list) -> None:
        flags.append(('enpassant', self.cor, self.caminho_acao))


class EnPassant(MovimentoComplexo):
    especial: bool = True

    def __init__(self, acao: tp.action, capturado_pos: tp. coord):
        """
        :param acao: movimento que o peão aliado fará
        * pos: posição do peão aliado
        * nova_pos: posição para o qual o peão aliado será movido
        :param capturado_pos: posição do peão inimigo a ser capturado
        """
        self.acao = acao
        self.capturado_pos = capturado_pos

    def executar(self, tabuleiro: tp. board, flags: list) -> None:
        mover_peca(tabuleiro, self.acao)
        i, j = self.capturado_pos
        tabuleiro[i][j] = None


class Peao(Peca):
    nome: str = 'peao'

    def __init__(self, cor: bool, movimentou: bool = False):
        super().__init__(cor)
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    # TODO type notation
    def _get_enpassant(
        self,
        flags: list,
        nova_pos
    ) -> tuple[tp.coord, tp.coord] | None:
        for flag in flags:
            match flag:
                case ['enpassant', cor, (_, meio, final)]:
                    if self.cor != cor and nova_pos == meio:
                        # Existe no máximo um enpassant por turno
                        return meio, final
        return None

    def _criar_captura(
        self,
        tabuleiro: tp.board,
        flags: list,
        acao: tp. action
    ) -> Movimento | None:
        i, j = acao.nova_pos
        promocao = 0 if self.cor else 7

        capturada = tabuleiro[i][j]
        if capturada is not None and capturada.cor != self.cor:
            if i == promocao:
                return Promocao(acao, self.cor)
            else:
                return Movimento(acao)
        else:
            enpassant = self._get_enpassant(flags, acao.nova_pos)
            if enpassant is not None:
                meio, final = enpassant
                return EnPassant(tp.action(acao.pos, final), meio)
            else:
                return None

    def get_movimentos_simples(
        self,
        tabuleiro: tp.board,
        flags: list,
        pos: tp.coord
    ) -> tp.movements:
        res = movements_vazio()
        linha_promocao = 0 if self.cor else 7

        i, j = pos
        i += -1 if self.cor else 1
        if tp. coord.valida_componente(i) and tabuleiro[i][j] is None:
            if i == linha_promocao:
                res[i][j] = Promocao(
                    tp. action(pos,  tp. coord(i, j)),
                    self.cor
                )
            else:
                res[i][j] = Avanco(self.cor, pos)

            ii = i-1 if self.cor else i+1
            avanco_duplo = (
                not self.movimentou
                and tp.coord.valida_componente(ii)
                and tabuleiro[ii][j] is None
            )
            if avanco_duplo:
                if i == linha_promocao:
                    res[ii][j] = Promocao(
                        tp.action(pos, tp.coord(ii, j)),
                        self.cor
                    )
                else:
                    res[ii][j] = AvancoDuplo(
                        self.cor,
                        tp.pathaction(pos, tp.coord(i, j), tp.coord(ii, j))
                    )

        i, j = pos
        i += -1 if self.cor else 1
        if tp.coord(i, j-1).valida():
            res[i][j-1] = self._criar_captura(
                tabuleiro,
                flags,
                tp. action(pos, tp. coord(i, j-1))
            )
        if tp.coord(i, j+1).valida():
            res[i][j+1] = self._criar_captura(
                tabuleiro,
                flags,
                tp. action(pos, tp.  coord(i, j+1))
            )

        return res
