from pygame.locals import *
from pygame import Surface
from pygame.event import Event

from util import tabuleiro_none, tabuleiro_false, tabuleiro_novo
from config import Config
from pecas import Pecas
from menu import Menu


class Xadrez:
    """Toda a lógica do jogo"""

    def __init__(self):
        self.atualizacao = True
        self.tabuleiro = tabuleiro_none()
        self.escape = False

        self.config = Config('marrom')
        self.pecas: Peca = Pecas()

        self.click = None
        self.movimento = None
        self.qsize = (0, 0)

    def carregar(self) -> None:
        self.pecas.carregar()
        self.tabuleiro = tabuleiro_novo(self.pecas)

    def event(self, event: Event) -> None:
        """
        Recebe um evento e executa uma operação com ele

        :param event: evento
        """

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            click_antigo = self.click

            i = int(event.pos[1] // self.qsize[1])
            j = int(event.pos[0] // self.qsize[0])

            self.click = (i, j)

            # Faz movimento
            if self.movimento and click_antigo:
                if isinstance(self.movimento[i][j], bool) and self.movimento[i][j]:
                    m, n = click_antigo
                    self.tabuleiro[i][j] = self.tabuleiro[m][n]
                    self.tabuleiro[m][n] = None

                    self.tabuleiro[i][j].notifica_movimento()
                elif isinstance(self.movimento[i][j], tuple):
                    movimento = (
                        i for i in self.movimento[i][j] if isinstance(i, tuple)
                    )

                    for mov in movimento:
                        (i, j), peca = mov
                        if peca is not None:
                            peca.notifica_movimento()
                        self.tabuleiro[i][j] = peca

                self.movimento = None

            # Atualiza movimentos
            if self.tabuleiro[i][j] is None:
                self.movimento = None
            else:
                self.movimento = self.tabuleiro[i][j].get_movimentos(
                    self.tabuleiro,
                    (i, j)
                )
            self.atualizacao = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.escape = True

    # TODO canva não é um bom nome para essa variavel
    # (pecas tambem usou o mesmo nome)
    def draw(self, canva) -> bool:
        """
        :param canva: Surface onde o jogo sera desenhado
        :return: Retorna se a tela precisa ser atualizada
        """

        size = canva.get_size()
        qsize = (size[0] / 8, size[1] / 8)
        self.qsize = qsize

        if self.atualizacao:
            for y, linha in enumerate(self.tabuleiro):
                for x, peca in enumerate(linha):
                    # j, i = x, y

                    tipo = 'vazio'
                    if self.click and y == self.click[0] and x == self.click[1]:
                        tipo = 'click'
                    elif self.movimento and self.movimento[y][x]:
                        tipo = 'movimento'

                    surf = self.config.quadrado(qsize, (x, y), tipo)

                    if peca:
                        peca.draw(surf)

                    pos = (qsize[0] * x, qsize[1] * y)
                    canva.blit(surf, pos)

            self.atualizacao = False
            return True
        else:
            return False

    def new(self):
        if self.escape:
            self.atualizacao = True
            self.escape = False
            menu = Menu(self)
            menu.carregar()
            return menu
        else:
            return None
