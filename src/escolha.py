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

        self.qsize = 0, 0

        self.pecas = [
            Cavalo(self.recursos, self.cor),
            Bispo(self.recursos, self.cor),
            Torre(self.recursos, self.cor),
            Rainha(self.recursos, self.cor)
        ]
        for i in self.pecas:
            i.notifica_movimento()

    ##### Interface #####
    def event(self, event: Event) -> None:
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # click esquerdo
            i = int(event.pos[1] // self.qsize[1])
            j = int(event.pos[0] // self.qsize[0])
            print(i, j)

            if i == 0 and 0 <= j - 2 < 4:
                self.escolhido = self.pecas[j - 2]
                print(self.escolhido)

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

        offset_i, offset_j = 0, 2
        for jj, peca in enumerate(self.pecas):
            # i, j = y, x
            i, j = offset_i, offset_j + jj

            surf = Surface(self.qsize)
            self.recursos.config.quadrado(surf, (j, i), 'vazio')
            peca.draw(surf)
            pos = j * self.qsize[0], i * self.qsize[1]
            canva.blit(surf, pos)

        self.atualizacao = False
        self.xadrez.atualizacao = True
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
            return Menu(self.recursos, self)
        else:
            return self
