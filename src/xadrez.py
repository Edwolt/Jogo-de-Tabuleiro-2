from pygame.locals import *
from pygame import display
from pygame import Surface
from pygame.event import Event

from util import tabuleiro_none, tabuleiro_false, tabuleiro_novo
from config import Config
from pecas import CriadorPecas
from movimentos import MovimentoEspecial
from menu import Menu


class Xadrez:
    """Toda a lógica do jogo"""

    def __init__(self):
        self.atualizacao = True
        self.tabuleiro = tabuleiro_none()
        self.escape = False
        self.flags = list()

        self.config = Config('bordas')
        self.criador_pecas: CriadorPecas = CriadorPecas()

        self.click = None
        self.movimento = None
        self.qsize = (0, 0)

    def movimenta_peca(self, pos, nova_pos) -> bool:
        """
        Movimenta a peça se o movimento for validao
        retornando se foi possível ou não

        :param pos: Posição da peça a ser movimentada
        :param nova_pos: Para onde será movimentada
        :return: Se a peça foi movimentada
        """

        l, c = pos
        m, n = nova_pos
        movimento = self.movimento[l][c]

        if isinstance(movimento, bool) and movimento:
            self.tabuleiro[l][c] = self.tabuleiro[m][n]
            self.tabuleiro[m][n] = None
            self.tabuleiro[l][c].notifica_movimento()

            self.flags.clear()
            return True

        elif isinstance(movimento, MovimentoEspecial):
            movimento.executar(self.tabuleiro, self.flags, self.criador_pecas)

            self.flags.clear()
            movimento.update_flags(self.flags)
            return True

        return False

    def atualiza_movimentos(self, pos) -> None:
        i, j = pos
        if self.tabuleiro[i][j] is None:
            self.movimento = None
        else:
            self.movimento = self.tabuleiro[i][j].get_movimentos(
                self.tabuleiro,
                self.flags,
                (i, j)
            )

    ##### Interface #####
    def carregar(self) -> None:
        self.criador_pecas.carregar()
        self.tabuleiro = tabuleiro_novo(self.criador_pecas)

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

        size = canva.get_size()
        self.qsize = (size[0] // 8, size[1] // 8)

        for y, linha in enumerate(self.tabuleiro):
            for x, peca in enumerate(linha):
                # j, i = x, y

                tipo = 'vazio'
                if self.click and y == self.click[0] and x == self.click[1]:
                    tipo = 'click'
                elif self.movimento and self.movimento[y][x]:
                    tipo = 'movimento'

                surf = Surface(self.qsize)
                self.config.quadrado(surf, (x, y), tipo)

                if peca:
                    peca.draw(surf)

                pos = (self.qsize[0] * x, self.qsize[1] * y)
                canva.blit(surf, pos)

        self.atualizacao = False
        display.flip()

    def new(self):
        if self.escape:
            self.atualizacao = True
            self.escape = False
            menu = Menu(self, self.config)
            menu.carregar()
            return menu
        else:
            return self
