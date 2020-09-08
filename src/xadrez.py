import pygame
from util import tabuleiro_none, tabuleiro_novo
from pecas import Pecas


class Xadrez:
    """Toda a lógica do jogo"""

    def __init__(self):
        self.atualizacao: bool = True
        self.tabuleiro: list = tabuleiro_none()
        self.cores: tuple = (
            (214, 165, 132),
            (124, 49, 0)
        )
        self.click_color: tuple = (153, 0, 0)
        self.click = None
        self.qsize: tuple = (0, 0)
        self.pecas = Pecas()

    def carregar(self):
        self.pecas.carregar()
        self.tabuleiro = tabuleiro_novo(self.pecas)

    def event(self, event: pygame.event) -> None:
        """
        Recebe um evento e executa uma operação com ele

        :param event: evento
        """

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click = (
                event.pos[0] // self.qsize[0],
                event.pos[1] // self.qsize[1]
            )
            self.atualizacao = True

    def draw(self, screen: pygame.Surface) -> bool:
        """
        :param screen: Surface onde sera desenhado o jogo sera desenhado
        :return: Retorna se a tela precisa ser atualizada
        """

        size = screen.get_size()
        qsize = (size[0] / 8, size[1] / 8)
        self.qsize = qsize

        if self.atualizacao:
            for x, linha in enumerate(self.tabuleiro):
                for y, peca in enumerate(linha):
                    surf = pygame.Surface(qsize)
                    color = self.cores[(x + y) % 2]
                    surf.fill(color)
                    pos = (qsize[0] * x, qsize[1] * y)
                    screen.blit(surf, pos)

            if self.click:
                surf = pygame.Surface(qsize)
                surf.fill(self.click_color)
                screen.blit(
                    surf, (self.click[0] * qsize[0], self.click[1] * qsize[1]))

            self.atualizacao = False
            return True
        else:
            return False
