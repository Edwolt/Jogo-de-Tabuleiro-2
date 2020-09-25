"""Movimentos Especiais"""


def mover_peca(tabuleiro: list, pos: tuple, nova_pos: tuple) -> None:
    i, j = pos
    m, n = nova_pos
    tabuleiro[m][n] = tabuleiro[i][j]
    tabuleiro[m][n].notifica_movimento()
    tabuleiro[i][j] = None


class MovimentoEspecial():
    """Classe abstrata para os movimentos especiais"""

    def executar(self, tabuleiro: list, criador_pecas, flags: list) -> None:
        """
        Executa o movimento no tabuleiro
        :param flags: lista de flags do tabuleiro
        """
        pass

    def update_flags(self, flags: list) -> None:
        """Atualiza a lista de flags do tabuleiro"""
        pass


class Roque(MovimentoEspecial):
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

    def executar(self, tabuleiro: list, flags: list, criador_pecas) -> None:
        mover_peca(tabuleiro, self.rei, self.nova_rei)
        mover_peca(tabuleiro, self.torre, self.nova_torre)


class Promocao(MovimentoEspecial):
    def __init__(self, pos: tuple, promocao: tuple):
        """
        :param pos: posição atual do peão
        :param promocao: posição para o qual o peão será movido causando a promoção
        """

        self.nome = 'promocao'
        self.pos = pos
        self.promocao = promocao
        pass

    def executar(self, tabuleiro: list, flags: list, criador_pecas) -> None:
        i, j = self.pos
        cor = tabuleiro[i][j].cor
        tabuleiro[i][j] = None

        i, j = self.promocao
        tabuleiro[i][j] = criador_pecas.Rainha(cor)


class AvancoDuplo(MovimentoEspecial):
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

    def executar(self, tabuleiro: list, flags: list, criador_pecas) -> None:
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


class EnPassant(MovimentoEspecial):
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

    def executar(self, tabuleiro: list, flags: list, criador_pecas) -> None:
        mover_peca(tabuleiro, self.pos, self.nova_pos)
        i, j = self.capturado_pos
        tabuleiro[i][j] = None
