from pygame.locals import *
from pygame import Surface
from pygame.event import Event

from config import Config
from util import tabuleiro_none, tabuleiro_false, tabuleiro_novo
from pecas import Pecas


class Xadrez:
    """Toda a lógica do jogo"""

    def __init__(self):
        self.atualizacao = True
        self.tabuleiro = tabuleiro_none()

        self.config = Config()
        self.pecas: Peca = Pecas()

        self.click = None
        self.movimento = tabuleiro_false()

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
            i = int(event.pos[1] // self.qsize[1])
            j = int(event.pos[0] // self.qsize[0])

            self.click = (i, j)

            if self.tabuleiro[i][j] is None:
                self.movimento = tabuleiro_false()
            else:
                self.movimento = self.tabuleiro[i][j].get_movimentos(self.tabuleiro, (i,j))

            self.atualizacao = True

    # TODO canva não é um bom nome para essa variavel (pecas tambem usou o mesmo nome)
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

                    surf = Surface(qsize)

                    tipo = 'vazio'
                    if self.click and y == self.click[0] and x == self.click[1]:
                        tipo = 'click'
                    elif self.movimento[y][x]:
                        tipo = 'movimento'

                    surf.fill(self.config.quadrado((x, y), tipo))

                    if peca:
                        peca.draw(surf)

                    pos = (qsize[0] * x, qsize[1] * y)
                    canva.blit(surf, pos)

            self.atualizacao = False
            return True
        else:
            return False
