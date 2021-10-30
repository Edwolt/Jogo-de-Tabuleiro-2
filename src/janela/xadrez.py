from pygame.locals import *
from pygame import display
from pygame import Surface
from pygame.event import Event

from recursos import Recursos
from tabuleiro import Tabuleiro
from janela.menu import Menu
from janela.escolha import Escolha
from janela.janela import Janela


class Xadrez(Janela):
    """Toda a lógica do jogo"""

    def __init__(self, recursos: Recursos):
        self.recursos = recursos

        self.atualizacao = True
        self.tabuleiro = Tabuleiro(self.recursos)
        self.escape = False
        self.promocao = None
        self.flags = list()

        self.click = None
        self.movimento = None
        self.qsize = 0, 0

    def atualiza_movimentos(self, pos: tuple[int, int]) -> None:
        self.movimento = self.tabuleiro.get_movimentos(pos)

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
                if self.tabuleiro.movimenta_peca(click_antigo, self.click, self.movimento):
                    self.movimento = None
                    movimentado = True

            if not movimentado:
                self.atualiza_movimentos(self.click)
            else:
                self.vez = not self.vez

            self.atualizacao = True

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.escape = True

    def draw(self, canvas: Surface) -> None:
        """
        :param canvas: Surface onde o jogo sera desenhado
        :return: Retorna se a tela precisa ser atualizada
        """

        if not self.atualizacao:
            return

        size = canvas.get_size()
        self.qsize = size[0] // 8, size[1] // 8

        self.tabuleiro.draw(canvas, self.click, self.movimento)

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
