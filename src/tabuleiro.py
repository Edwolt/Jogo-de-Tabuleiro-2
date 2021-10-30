from pygame import Surface

from types import SimpleNamespace

from recursos import Recursos
from pecas import Rei, Rainha, Bispo, Cavalo, Torre, Peao
from pecas import testar_xeque
from pecas import MovimentoEspecial


def novo_tabuleiro(recursos: Recursos) -> list[list[None]]:
    """
    :param pecas: objeto da classe Peca
    :return: list 8x8 onde os espacos vazios valem None
    e os espacos com pecas são objetos
    """
    tabuleiro = [[None] * 8 for _ in range(8)]  # list 8x8 com None

    # Pretas
    tabuleiro[0][0] = Torre(recursos, False)
    tabuleiro[0][1] = Cavalo(recursos, False)
    tabuleiro[0][2] = Bispo(recursos, False)
    tabuleiro[0][3] = Rainha(recursos, False)
    tabuleiro[0][4] = Rei(recursos, False)
    tabuleiro[0][5] = Bispo(recursos, False)
    tabuleiro[0][6] = Cavalo(recursos, False)
    tabuleiro[0][7] = Torre(recursos, False)
    for i in range(8):  # Peões
        tabuleiro[1][i] = Peao(recursos, False)

    # Brancas
    tabuleiro[7][0] = Torre(recursos, True)
    tabuleiro[7][1] = Cavalo(recursos, True)
    tabuleiro[7][2] = Bispo(recursos, True)
    tabuleiro[7][3] = Rainha(recursos, True)
    tabuleiro[7][4] = Rei(recursos, True)
    tabuleiro[7][5] = Bispo(recursos, True)
    tabuleiro[7][6] = Cavalo(recursos, True)
    tabuleiro[7][7] = Torre(recursos, True)
    for i in range(8):  # Peões
        tabuleiro[6][i] = Peao(recursos, True)

    return tabuleiro


class Tabuleiro:
    def __init__(self, recursos: Recursos):
        self.recursos = recursos  # TODO tranformar recursos em um Singleton

        self.tabuleiro = novo_tabuleiro()
        self.vez = True
        self.flags = list()
        self.rei = SimpleNamespace(branco=(7, 4), preto=(0, 4))

    def movimenta_peca(self, pos: tuple[int, int], nova_pos: tuple[int, int], movimento: list[list]) -> bool:
        """
        Movimenta a peça se o movimento for validao
        retornando se foi possível ou não

        :param pos: Posição da peça a ser movimentada
        :param nova_pos: Para onde será movimentada
        :return: Se a peça foi movimentada
        """

        i, j = pos
        m, n = nova_pos

        if isinstance(movimento, bool) and movimento:
            self.tabuleiro[m][n] = self.tabuleiro[i][j]
            self.tabuleiro[i][j] = None
            self.tabuleiro[m][n].notifica_movimento()

            if self.rei.branco == pos:
                self.rei.branco = nova_pos
            elif self.rei.preto == pos:
                self.rei.preto = nova_pos

            self.flags.clear()
            return True

        elif isinstance(movimento, MovimentoEspecial):
            movimento.executar(self.tabuleiro, self.flags, self.recursos)

            if movimento.nome == 'roque':
                if self.rei.branco == movimento.rei:
                    self.rei.branco = movimento.nova_rei
                elif self.rei.preto == movimento.rei:
                    self.rei.preto = movimento.nova_rei
            elif movimento.nome == 'promocao':
                self.promocao = movimento

            self.flags.clear()
            movimento.update_flags(self.flags)
            return True

        return False

    def get_movimentos(self, pos: tuple[int, int]) -> 'list[list] | None':
        i, j = pos
        peca = self.tabuleiro[i][j]
        if peca is None:
            return None
        elif peca.cor == self.vez:
            return peca.get_movimentos(
                self.tabuleiro,
                self.flags,
                self.rei.braco if self.vez else self.rei.preto,
                pos
            )
        else:
            return None

    def draw(self, canvas: Surface, click: 'tuple[int, int] | None', movimento: list[list]) -> None:
        size = canvas.get_size()
        size = size[0] // 8, size[1] // 8

        for y, linha in enumerate(self.tabuleiro):
            for x, peca in enumerate(linha):
                # i, j = y, x

                tipo = 'vazio'
                if click and (y, x) == click:
                    tipo = 'click'
                elif movimento and movimento[y][x]:
                    if isinstance(movimento[y][x], MovimentoEspecial) and movimento[y][x].nome in ('roque', 'enpassant', 'avancoduplo'):
                        tipo = 'especial'
                    else:
                        tipo = 'movimento'
                elif ((y, x) == self.rei.branco or (y, x) == self.rei.preto) and testar_xeque(self.tabuleiro, self.flags, (y, x)):
                    tipo = 'xeque'

                surf = Surface(size)
                self.recursos.config.quadrado(surf, (x, y), tipo)

                if peca:
                    peca.draw(surf)

                pos = x * size[0], y * size[1]
                canvas.blit(surf, pos)
