from pygame.locals import *
from pygame import display
from pygame import Surface
from pygame.event import Event

from recursos import Recursos
from pecas import MovimentoEspecial
from menu import Menu


class Escolha():
    def __init__(self, recursos: Recursos, xadrez, promocao: MovimentoEspecial):
        """
        Permite o usuário Escolher um peça entre:
        * Cavalo
        * Bispo
        * Torre
        * Rainha
        """
        self.recursos = recursos
        self.xadrez = xadrez
        self.promocao = promocao

        self.atualizacao = True
        self.escolhido = None
        self.escape = False

        self.click = None
        self.qsize = 0, 0

    ##### Interface #####
    def event(self, event: Event) -> None:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # click esquerdo
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.escape = True

    def draw(self, canva: Surface) -> None:
        if not self.atualizacao:
            return

        canva.fill(Color(0, 0, 0))
        size = canva.get_size()
        surf = Surface((size[0], size[1]//8 * 6))
        self.xadrez.draw(surf)
        canva.blit(surf, (0, size[1]//8 * 2))

        self.atualizacao = False
        display.set_caption(self.recursos.config.titulo(self.promocao.cor))
        display.flip()

    def new(self):
        if self.escolhido:
            i, j = self.promocao.promocao
            self.xadrez.tabuleiro[i][j] = self.escolhido
            print(self.escolhido)
            return self.xadrez
        elif self.escape:
            self.escape = False
            self.atualizacao = True
            self.xadrez.atualizacao = True
            return Menu(self.recursos, self)
        else:
            return self
