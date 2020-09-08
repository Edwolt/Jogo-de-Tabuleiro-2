import pygame
from xadrez import Xadrez

Jogo = None
size = (800, 800)

if __name__ == 'main':
    Jogo = Xadrez()

    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            Jogo.event(evento)

        if Jogo.draw(screen):
            # Nao estou usando o update por que provavelmente toda tela será atualizada
            pygame.display.flip()
