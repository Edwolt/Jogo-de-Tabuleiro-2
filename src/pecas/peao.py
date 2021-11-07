from tipos import board, movements, pb, coord, action, pathaction

from .abc_peca import Peca
from .abc_movimento import MovimentoEspecial
from .util import mover_peca, tabuleiro_false


class Promocao(MovimentoEspecial):
    def __init__(self, acao: action, cor: bool):
        """
        :param pos: posição atual do peão
        :param promocao: posição para o qual o peão será movido causando a promoção
        """

        super().__init__(nome='promocao')
        self.pos = acao.pos
        self.promocao = acao.nova_pos
        self.cor = cor
        pass

    def executar(self, tabuleiro: board, flags: list) -> None:
        i, j = self.pos
        m, n = self.promocao
        tabuleiro[m][n] = tabuleiro[i][j]
        tabuleiro[i][j] = None
        tabuleiro[m][n].notifica_movimento()


class Avanco(MovimentoEspecial):
    def __init__(self, cor: bool, pos: coord):
        super().__init__(nome='avanco', avanco=True)
        self.cor = cor
        self.pos = pos

    def executar(self, tabuleiro: board, flags: list):
        i, j = self.pos
        i += -1 if self.cor else 1
        mover_peca(tabuleiro, action(self.pos, coord(i, j)))


class AvancoDuplo(MovimentoEspecial):
    def __init__(self, cor: bool, acao: pathaction):
        """
        :param cor: cor da peça (True: 'branco'; False: 'preto')
        :param pos: posição do peão
        :param meio: posição pela qual o peão passará
        :param nova_pos: posição final do peão
        """

        super().__init__(nome='avancoduplo', avanco=True)
        self.cor = cor
        self.acao = acao

    def executar(self, tabuleiro: board, flags: list) -> None:
        mover_peca(tabuleiro, self.acao.to_action())

    def update_flags(self, flags: list) -> None:
        flags.append(('enpassant', self.cor, self.acao))


class EnPassant(MovimentoEspecial):
    def __init__(self, acao: action, capturado_pos: coord):
        """
        :param pos: posição do peão aliado
        :param capturado_pos: posição do peão inimigo a ser capturado
        :param nova_pos: posição para o qual o peão aliado será movido
        """

        super().__init__(nome='enpassant')
        self.acao = acao
        self.capturado_pos = capturado_pos

    def executar(self, tabuleiro: board, flags: list) -> None:
        mover_peca(tabuleiro, self.acao)
        i, j = self.capturado_pos
        tabuleiro[i][j] = None


class Peao(Peca):
    def __init__(self, cor: bool, movimentou: bool = False):
        super().__init__(cor, nome='peao')
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def get_enpassant(self, flags: list, nova_pos):
        for flag in flags:
            if flag[0] == 'enpassant':
                _, cor, (_, meio, final) = flag
                if self.cor != cor and nova_pos == meio:
                    return meio, final
        return None

    def criar_captura(self, tabuleiro: board, flags: list, acao: action):
        i, j = acao.nova_pos
        promocao = 0 if self.cor else 7

        if tabuleiro[i][j] is not None and tabuleiro[i][j].cor != self.cor:
            if i == promocao:
                return Promocao(acao, self.cor)
            else:
                return True
        else:
            enpassant = self.get_enpassant(flags, acao.nova_pos)
            if enpassant is not None:
                meio, final = enpassant
                return EnPassant(action(acao.pos, final), meio)
            else:
                return False

    def get_movimentos_simples(self, tabuleiro: board, flags: list, pos: coord) -> movements:
        res = tabuleiro_false()
        linha_promocao = 0 if self.cor else 7

        i, j = pos
        i += -1 if self.cor else 1
        if coord.valida_componente(i) and tabuleiro[i][j] is None:
            if i == linha_promocao:
                res[i][j] = Promocao(action(pos, coord(i, j)), self.cor)
            else:
                res[i][j] = Avanco(self.cor, pos)

            ii = i-1 if self.cor else i+1
            if not self.movimentou and coord.valida_componente(ii) and tabuleiro[ii][j] is None:
                if i == linha_promocao:
                    res[ii][j] = Promocao(pos, (ii, j), self.cor)
                else:
                    res[ii][j] = AvancoDuplo(self.cor, pos, (i, j), (ii, j))

        i, j = pos
        i += -1 if self.cor else 1
        if coord(i, j-1).valida():
            res[i][j-1] = self.criar_captura(
                tabuleiro,
                flags,
                action(pos, coord(i, j-1))
            )
        if coord(i, j+1).valida():
            res[i][j+1] = self.criar_captura(
                tabuleiro,
                flags,
                action(pos, coord(i, j+1))
            )

        return res
