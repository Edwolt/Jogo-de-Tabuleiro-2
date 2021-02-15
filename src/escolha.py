from pygame.locals import *
from pygame import display
from pygame import Surface
from pygame.event import Event

from recursos import Recursos
from pecas import Cavalo, Bispo, Torre, Rainha
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
        self.cor = self.promocao.cor

        self.atualizacao = True
        self.escolhido = None
        self.escape = False

        self.click = None
        self.qsize = 0, 0

        self.cavalo = Cavalo(self.recursos, self.cor)
        self.cavalo.notifica_movimento()
        self.bispo = Bispo(self.recursos, self.cor)
        self.bispo.notifica_movimento()
        self.torre = Torre(self.recursos, self.cor)
        self.torre.notifica_movimento()
        self.rainha = Rainha(self.recursos, self.cor)
        self.rainha.notifica_movimento()

    ##### Interface #####
    def event(self, event: Event) -> None:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # click esquerdo
            return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            self.escape = True

    def draw(self, canva: Surface) -> None:
        if not self.atualizacao:
            return

        size = canva.get_size()
        self.qsize = size[0] // 8, size[1] // 8

        canva.fill(Color(0, 0, 0))
        tabuleiro = Surface((6 * self.qsize[0], 6 * self.qsize[1]))
        self.xadrez.draw(tabuleiro)
        canva.blit(tabuleiro, (self.qsize[0], 2 * self.qsize[1]))

        # i, j = y, x
        i, j = 0, 2
        surf = Surface(self.qsize)
        self.recursos.config.quadrado(surf, (j, i), 'vazio')
        self.cavalo.draw(surf)
        pos = j * self.qsize[0], i * self.qsize[1]
        canva.blit(surf, pos)

        i, j = 0, 3
        surf = Surface(self.qsize)
        self.recursos.config.quadrado(surf, (j, i), 'vazio')
        self.bispo.draw(surf)
        pos = j * self.qsize[0], i * self.qsize[1]
        canva.blit(surf, pos)

        i, j = 0, 4
        surf = Surface(self.qsize)
        self.recursos.config.quadrado(surf, (j, i), 'vazio')
        self.torre.draw(surf)
        pos = j * self.qsize[0], i * self.qsize[1]
        canva.blit(surf, pos)

        i, j = 0, 5
        surf = Surface(self.qsize)
        self.recursos.config.quadrado(surf, (j, i), 'vazio')
        self.rainha.draw(surf)
        pos = j * self.qsize[0], i * self.qsize[1]
        canva.blit(surf, pos)

        self.atualizacao = False
        display.set_caption(self.recursos.config.titulo(self.cor))
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
