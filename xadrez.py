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
        self.click_color = (153, 0, 0)
        self.__click = None

    def event(self, event: pygame.event) -> None:
        """
        Recebe um evento e executa uma operação com ele

        :param event: evento
        """
        pass

    def draw(self, screen: pygame.Surface) -> bool:
        """
        :param screen: Surface onde sera desenhado o jogo sera desenhado
        :return: Retorna se houve mudança ou nao na tela
        """

        size = screen.get_size()
        qsize = (size[0] / 8, size[1] / 8)

        if self.__atualizacao:
            for x, linha in enumerate(self.__tabuleiro):
                for y, peca in enumerate(linha):
                    surf = pygame.Surface(qsize)
                    color = self.cores[(x + y) % 2]
                    surf.fill(color)
                    pos = (qsize[0] * x, qsize[1] * y)
                    screen.blit(surf, pos)

            self.__atualizacao = False
            return True
        else:
            return False
