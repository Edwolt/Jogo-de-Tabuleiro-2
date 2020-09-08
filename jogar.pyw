import pygame
from xadrez import Xadrez

Jogo = None
size = (800, 800)
framerate = 60

print('funciona por favor')

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    Jogo = Xadrez()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            Jogo.event(event)

        if Jogo.draw(screen):
            pygame.display.flip()  # Atualiza toda tela (para atualizar função tem o update)

        clock.tick(framerate)
