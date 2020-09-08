import pygame


class Xadrez:
    """Toda a lógica do jogo"""

    def __init__(self):
        self.__atualizacao: bool = True
        self.__tabuleiro = [[None] * 8 for _ in range(8)]
        self.cores = [
            (214, 165, 132),
            (124, 49, 0)
        ]

    def event(self, event: pygame.event) -> None:
        """
        Recebe um evento e executa uma operação com ele

        :param event: evento
        """
        pass

    def draw(self, screen: pygame.surface) -> bool:
        """[summary]
        :param screen: Surface onde sera desenhado o jogo sera desenhado
        :return: Retorna se houve mudança ou nao na tela
        """

        size = screen.get_size()
        quad_size = (size[0] / 8, size[1] / 8)

        if self.__atualizacao:
            for x, i in enumerate(self.__tabuleiro):
                for y, j in enumerate(i):
                    quad_surf = pygame.Surface(quad_size)
                    color = self.cores[(x + y) % 2]
                    quad_surf.fill(color)
                    pos = (quad_size[0] * x, quad_size[1]*y)
                    screen.blit(quad_surf, pos)

            self.__atualizacao = False
            return True
        else:
            return False
