from recursos import Recursos
from pecas import Peca, MovimentoEspecial
from .util import mover_peca, tabuleiro_false, valida_coordenadas


class Promocao(MovimentoEspecial):
    def __init__(self, pos: tuple[int, int], promocao: tuple[int, int], cor: bool):
        """
        :param pos: posição atual do peão
        :param promocao: posição para o qual o peão será movido causando a promoção
        """

        super().__init__(nome='promocao')

        self.nome = 'promocao'
        self.pos = pos
        self.cor = cor
        self.promocao = promocao
        pass

    def executar(self, tabuleiro: list[list], flags: list, recursos: Recursos) -> None:
        i, j = self.pos
        m, n = self.promocao
        tabuleiro[m][n] = tabuleiro[i][j]
        tabuleiro[i][j] = None
        tabuleiro[m][n].notifica_movimento()


class Avanco(MovimentoEspecial):
    def __init__(self, cor: bool, pos: tuple[int, int]):
        super().__init__(nome='avanco', avanco=True)
        self.cor = cor
        self.pos = pos

    def executar(self, tabuleiro: list[list], flags: list, recursos: Recursos):
        i, j = self.pos
        i += -1 if self.cor else 1
        mover_peca(tabuleiro, self.pos, (i, j))


class AvancoDuplo(MovimentoEspecial):
    def __init__(self, cor: bool, pos: tuple[int, int], meio: tuple[int, int], nova_pos: tuple[int, int]):
        """
        :param cor: cor da peça (True: 'branco'; False: 'preto')
        :param pos: posição do peão
        :param meio: posição pela qual o peão passará
        :param nova_pos: posição final do peão
        """

        super().__init__(nome='avancoduplo', avanco=True)
        self.cor = cor
        self.pos = pos
        self.meio = meio
        self.nova_pos = nova_pos

    def executar(self, tabuleiro: list[list], flags: list, recursos: Recursos) -> None:
        mover_peca(tabuleiro, self.pos, self.nova_pos)

    def update_flags(self, flags: list) -> None:
        flags.append(('enpassant', self.cor, self.meio, self.nova_pos))


class EnPassant(MovimentoEspecial):
    def __init__(self, pos: tuple[int, int], capturado_pos: tuple[int, int], nova_pos: tuple[int, int]):
        """
        :param pos: posição do peão aliado
        :param capturado_pos: posição do peão inimigo a ser capturado
        :param nova_pos: posição para o qual o peão aliado será movido
        """

        super().__init__(nome='enpassant')
        self.pos = pos
        self.capturado_pos = capturado_pos
        self.nova_pos = nova_pos

    def executar(self, tabuleiro: list[list], flags: list, recursos: Recursos) -> None:
        mover_peca(tabuleiro, self.pos, self.nova_pos)
        i, j = self.capturado_pos
        tabuleiro[i][j] = None


class Peao(Peca):
    def __init__(self, recursos: Recursos, cor: bool, movimentou: bool = False):
        super().__init__(recursos, cor, nome='peao')
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

    def criar_captura(self, tabuleiro: list[list], flags: list, pos: tuple[int, int], nova_pos: tuple[int, int]):
        i, j = nova_pos
        promocao = 0 if self.cor else 7

        if tabuleiro[i][j] is not None and tabuleiro[i][j].cor != self.cor:
            if i == promocao:
                return Promocao(pos, nova_pos, self.cor)
            else:
                return True
        else:
            enpassant = self.get_enpassant(flags, nova_pos)
            if enpassant is not None:
                meio, final = enpassant
                return EnPassant(pos, final, meio)
            else:
                return False

    def get_movimentos_simples(self, tabuleiro: list[list], flags: list, pos: tuple[int, int]) -> list[list]:
        res = tabuleiro_false()
        promocao = 0 if self.cor else 7

        i, j = pos
        i += -1 if self.cor else 1
        if valida_coordenadas(i) and tabuleiro[i][j] is None:
            if i == promocao:
                res[i][j] = Promocao(pos, (i, j), self.cor)
            else:
                res[i][j] = Avanco(self.cor, pos)

            ii = i-1 if self.cor else i+1
            if not self.movimentou and valida_coordenadas(ii) and tabuleiro[ii][j] is None:
                if i == promocao:
                    res[ii][j] = Promocao(pos, (ii, j), self.cor)
                else:
                    res[ii][j] = AvancoDuplo(self.cor, pos, (i, j), (ii, j))

        i, j = pos
        i += -1 if self.cor else 1
        if valida_coordenadas(i, j-1):
            res[i][j-1] = self.criar_captura(tabuleiro, flags, pos, (i, j-1))
        if valida_coordenadas(i, j+1):
            res[i][j+1] = self.criar_captura(tabuleiro, flags, pos, (i, j+1))

        return res
