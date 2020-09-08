import pygame
from util import tabuleiro_none


class Xadrez:
    """Toda a lógica do jogo"""

    def __init__(self):
        self.__atualizacao: bool = True
        self.__tabuleiro: list = tabuleiro_none()
        self.cores: tuple = (
            (214, 165, 132),
            (124, 49, 0)
        )
        self.click_color: tuple = (153, 0, 0)
        self.__click = None
        self.__qsize: tuple = (0, 0)

    def event(self, event: pygame.event) -> None:
        """
        Recebe um evento e executa uma operação com ele

        :param event: evento
        """

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.__click = (
                event.pos[0] // self.__qsize[0],
                event.pos[1] // self.__qsize[1]
            )
            self.__atualizacao = True

    def draw(self, screen: pygame.Surface) -> bool:
        """
        :param screen: Surface onde sera desenhado o jogo sera desenhado
        :return: Retorna se houve mudança ou nao na tela
        """

        size = screen.get_size()
        qsize = (size[0] / 8, size[1] / 8)
        self.__qsize = qsize

        if self.__atualizacao:
            for x, linha in enumerate(self.__tabuleiro):
                for y, peca in enumerate(linha):
                    surf = pygame.Surface(qsize)
                    color = self.cores[(x + y) % 2]
                    surf.fill(color)
                    pos = (qsize[0] * x, qsize[1] * y)
                    screen.blit(surf, pos)

            if self.__click:
                surf = pygame.Surface(qsize)
                surf.fill(self.click_color)
                screen.blit(
                    surf, (self.__click[0] * qsize[0], self.__click[1] * qsize[1]))

            self.__atualizacao = False
            return True
        else:
            return False
