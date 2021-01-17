from pygame.locals import *
from pygame import display, draw
from pygame import Surface
from pygame.event import Event

from pecas import Rei, Rainha, Bispo, Cavalo, Torre, Peao
from pecas import verifica_xeque, tabuleiro_xeque
from recursos import Recursos
from pecas import MovimentoEspecial
from menu import Menu


def tabuleiro_novo(recursos: Recursos) -> list:
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
        self.flags = list()

        self.click = None
        self.movimento = None
        self.qsize = 0, 0
        self.vez = True

    def movimenta_peca(self, pos: tuple, nova_pos: tuple) -> bool:
        """
        Movimenta a peça se o movimento for validao
        retornando se foi possível ou não

        :param pos: Posição da peça a ser movimentada
        :param nova_pos: Para onde será movimentada
        :return: Se a peça foi movimentada
        """

        i, j = pos
        m, n = nova_pos
        movimento = self.movimento[i][j]

        if isinstance(movimento, bool) and movimento:
            self.tabuleiro[i][j] = self.tabuleiro[m][n]
            self.tabuleiro[m][n] = None
            self.tabuleiro[i][j].notifica_movimento()

            if self.tabuleiro[i][j].nome == 'rei':
                cor = 'branco' if self.tabuleiro[i][j].cor else 'preto'
                self.rei[cor] = (i, j)

            self.flags.clear()
            return True

        elif isinstance(movimento, MovimentoEspecial):
            movimento.executar(self.tabuleiro, self.flags, self.recursos)

            if movimento.nome == 'roque':
                ri, rj = movimento.nova_rei
                cor = 'branco' if self.tabuleiro[ri][rj].cor else 'preto'
                self.rei[cor] = movimento.nova_rei

            self.flags.clear()
            movimento.update_flags(self.flags)
            return True

        return False

    def atualiza_movimentos(self, pos: tuple) -> None:
        i, j = pos
        peca = self.tabuleiro[i][j]
        if peca is None:
            self.movimento = None
        elif peca.cor == self.vez:
            self.movimento = peca.get_movimentos(
                self.tabuleiro,
                self.flags,
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
                if self.movimenta_peca(self.click, click_antigo):
                    self.movimento = None
                    movimentado = True

            if not movimentado:
                self.atualiza_movimentos(self.click)
            else:
                self.vez = not self.vez
                for i, linha in enumerate(self.tabuleiro):
                    for j, peca in enumerate(linha):
                        if peca is not None and peca.cor == self.vez and peca.nome == 'rei':
                            print(f'verificando rei {peca.cor} em {i} {j}')
                            verifica_xeque(self.tabuleiro, self.flags, (i, j))

            self.atualizacao = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.escape = True

    def draw(self, canva) -> None:
        """
        :param canva: Surface onde o jogo sera desenhado
        :return: Retorna se a tela precisa ser atualizada
        """

        if not self.atualizacao:
            return

        # TODO limpar esse trecho do código
        xeque_branco = tabuleiro_xeque(
            self.tabuleiro,
            self.flags,
            self.rei['branco']
        )
        xeque_preto = tabuleiro_xeque(
            self.tabuleiro,
            self.flags,
            self.rei['preto']
        )

        size = canva.get_size()
        self.qsize = size[0] // 8, size[1] // 8

        for y, linha in enumerate(self.tabuleiro):
            for x, peca in enumerate(linha):
                # j, i = x, y

                tipo = 'vazio'
                if self.click and y == self.click[0] and x == self.click[1]:
                    tipo = 'click'
                elif self.movimento and self.movimento[y][x]:
                    tipo = 'movimento'

                surf = Surface(self.qsize)
                self.recursos.config.quadrado(surf, (x, y), tipo)

                # TODO limpar esse trecho do código
                if xeque_branco[y][x]:
                    if self.tabuleiro[y][x] is not None and self.tabuleiro[y][x].nome == 'rei':
                        draw.circle(
                            surf,
                            (255, 100, 100),
                            (self.qsize[0]/2, self.qsize[1]/2),
                            self.qsize[0]/3
                        )
                    else:
                        draw.circle(
                            surf,
                            (255, 255, 255),
                            (self.qsize[0]/2, self.qsize[1]/2),
                            self.qsize[0]/3
                        )
                if xeque_preto[y][x]:
                    if self.tabuleiro[y][x] is not None and self.tabuleiro[y][x].nome == 'rei':
                        draw.circle(
                            surf,
                            (100, 0, 0),
                            (self.qsize[0]/2, self.qsize[1]/2),
                            self.qsize[0]/4
                        )
                    else:
                        draw.circle(
                            surf,
                            (0, 0, 0),
                            (self.qsize[0]/2, self.qsize[1]/2),
                            self.qsize[0]/4
                        )

                if peca:
                    peca.draw(surf)

                pos = x * self.qsize[0], y * self.qsize[1]
                canva.blit(surf, pos)

        self.atualizacao = False
        display.flip()
        display.set_caption(self.recursos.config.titulo(self.vez))

    def new(self):
        if self.escape:
            self.atualizacao = True
            self.escape = False
            return Menu(self.recursos, self)
        else:
            return self
