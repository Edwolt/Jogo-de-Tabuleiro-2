import pygame


class Xadrez:
    """Toda a lógica do jogo"""

    screen = property()

    @screen.setter
    def screen(self, value: pygame.Surface):
        size = value.get_size()
        self.__quad_size = (size[0] / 8, size[1] / 8)
        self.__screen = value

    @screen.getter
    def screen(self):
        return self.__screen

    def __init__(self, screen: pygame.Surface):
        self.__atualizacao: bool = True
        self.__tabuleiro = [[None] * 8 for _ in range(8)]
        self.cores = [
            (214, 165, 132),
            (124, 49, 0)
        ]
        self.click_color = (153, 0, 0)
        self.__click = None

        self.__quad_size = (0, 0)
        self.__screen = None
        self.screen = screen

    def event(self, event: pygame.event) -> None:
        """
        Recebe um evento e executa uma operação com ele

        :param event: evento
        """
        pass

    def draw(self) -> bool:
        """[summary]
        :param screen: Surface onde sera desenhado o jogo sera desenhado
        :return: Retorna se houve mudança ou nao na tela
        """

        if self.__atualizacao:
            for x, i in enumerate(self.__tabuleiro):
                for y, j in enumerate(i):
                    quad_surf = pygame.Surface(self.__quad_size)
                    color = self.cores[(x + y) % 2]
                    quad_surf.fill(color)
                    pos = (self.__quad_size[0] * x, self.__quad_size[1]*y)
                    self.screen.blit(quad_surf, pos)

            self.__atualizacao = False
            return True
        else:
            return False
