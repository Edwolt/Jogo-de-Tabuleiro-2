import pygame
from xadrez import Xadrez


size = (800, 800)
framerate = 60

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    xadrez = Xadrez()
    xadrez.carregar()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            xadrez.event(event)

        if xadrez.draw(screen):
            pygame.display.flip()  # Atualiza toda tela (para atualizar função tem o update)

        clock.tick(framerate)
