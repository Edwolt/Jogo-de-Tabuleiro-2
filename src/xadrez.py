from pygame.locals import *
from pygame import display
from pygame import Surface
from pygame.event import Event

from recursos import Recursos
from pecas import Rei, Rainha, Bispo, Cavalo, Torre, Peao
from pecas import testar_xeque
from pecas import MovimentoEspecial
from menu import Menu
from escolha import Escolha


def tabuleiro_novo(recursos: Recursos) -> list[list[None]]:
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


class Xadrez:
    """Toda a lógica do jogo"""

    def __init__(self, recursos: Recursos):
        self.recursos = recursos

        self.atualizacao = True
        self.tabuleiro = tabuleiro_novo(self.recursos)
        self.rei = {'branco': (7, 4), 'preto': (0, 4)}
        self.escape = False
        self.promocao = None
        self.flags = list()

        self.click = None
        self.movimento = None
        self.qsize = 0, 0
        self.vez = True

    def movimenta_peca(self, pos: tuple[int, int], nova_pos: tuple[int, int]) -> bool:
        """
        Movimenta a peça se o movimento for validao
        retornando se foi possível ou não

        :param pos: Posição da peça a ser movimentada
        :param nova_pos: Para onde será movimentada
        :return: Se a peça foi movimentada
        """

        i, j = pos
        m, n = nova_pos
        movimento = self.movimento[m][n]

        if isinstance(movimento, bool) and movimento:
            self.tabuleiro[m][n] = self.tabuleiro[i][j]
            self.tabuleiro[i][j] = None
            self.tabuleiro[m][n].notifica_movimento()

            if self.rei['branco'] == pos:
                self.rei['branco'] = nova_pos
            elif self.rei['preto'] == pos:
                self.rei['preto'] = nova_pos

            self.flags.clear()
            return True

        elif isinstance(movimento, MovimentoEspecial):
            movimento.executar(self.tabuleiro, self.flags, self.recursos)

            if movimento.nome == 'roque':
                if self.pos_rei['branco'] == movimento.rei:
                    self.pos_rei['branco'] = movimento.nova_rei
                elif self.pos_rei['preto'] == movimento.rei:
                    self.pos_rei['preto'] = movimento.nova_rei
            elif movimento.nome == 'promocao':
                self.promocao = movimento

            self.flags.clear()
            movimento.update_flags(self.flags)
            return True

        return False

    def atualiza_movimentos(self, pos: tuple[int, int]) -> None:
        i, j = pos
        peca = self.tabuleiro[i][j]
        if peca is None:
            self.movimento = None
        elif peca.cor == self.vez:
            self.movimento = peca.get_movimentos(
                self.tabuleiro,
                self.flags,
                self.rei['branco' if self.vez else 'preto'],
                (i, j)
            )
        else:
            self.movimento = None

    ##### Interface #####
    def event(self, event: Event) -> None:
        """
        Recebe um evento e executa uma operação com ele
        :param event: evento
        """

        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # click esquerdo
            click_antigo = self.click

            self.click = (
                int(event.pos[1] // self.qsize[1]),
                int(event.pos[0] // self.qsize[0])
            )

            movimentado = False
            if self.movimento and click_antigo:
                if self.movimenta_peca(click_antigo, self.click):
                    self.movimento = None
                    movimentado = True

            if not movimentado:
                self.atualiza_movimentos(self.click)
            else:
                self.vez = not self.vez

            self.atualizacao = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.escape = True

    def draw(self, canva: Surface) -> None:
        """
        :param canva: Surface onde o jogo sera desenhado
        :return: Retorna se a tela precisa ser atualizada
        """

        if not self.atualizacao:
            return

        size = canva.get_size()
        self.qsize = size[0] // 8, size[1] // 8

        for y, linha in enumerate(self.tabuleiro):
            for x, peca in enumerate(linha):
                # i, j = y, x

                tipo = 'vazio'
                if self.click and (y, x) == self.click:
                    tipo = 'click'
                elif self.movimento and self.movimento[y][x]:
                    if isinstance(self.movimento[y][x], MovimentoEspecial) and self.movimento[y][x].nome in ('roque', 'enpassant', 'avancoduplo'):
                        tipo = 'especial'
                    else:
                        tipo = 'movimento'
                elif ((y, x) == self.rei['branco'] or (y, x) == self.rei['preto']) and testar_xeque(self.tabuleiro, self.flags, (y, x)):
                    tipo = 'xeque'

                surf = Surface(self.qsize)
                self.recursos.config.quadrado(surf, (x, y), tipo)

                if peca:
                    peca.draw(surf)

                pos = x * self.qsize[0], y * self.qsize[1]
                canva.blit(surf, pos)

        self.atualizacao = False
        display.set_caption(self.recursos.config.titulo(self.vez))
        display.flip()

    def new(self):
        if self.escape:
            self.atualizacao = True
            self.escape = False
            return Menu(self.recursos, self)
        elif self.promocao is not None:
            self.atualizacao = True
            promocao = self.promocao
            self.promocao = None
            return Escolha(self.recursos, self, promocao)
        else:
            return self
