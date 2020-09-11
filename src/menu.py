import pygame
from pygame.font import Font
from pygame import Surface
from pygame.event import Event
from pygame.locals import *


class Menu:
    def __init__(self, xadrez):
        self.xadrez = xadrez

        self.atualizacao = True
        self.fonte = Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            50
        )
        self.opcoes = [
            'Config',
            'Imagens',
            'Fonte',
            'Desfazer',
            'Voltar',
            'Sair'
        ]

        self.sel = 0

    def carregar(self):
        return

    def event(self, event: Event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if self.sel > 0:
                    self.sel -= 1
                else:
                    self.sel = len(self.opcoes) - 1
            elif event.key == K_DOWN:
                if self.sel < len(self.opcoes) - 1:
                    self.sel += 1
                else:
                    self.sel = 0
            elif event.key == pygame.K_RETURN:
                opcao = self.opcoes(self.sel)
                if opcao == 'Sair':
                    pygame.quit()
                    quit(0)
                else:
                    print(f'opção nao executada: {opcao}')

    def draw(self, canva: Surface):
        canva.fill((0, 0, 0))

        _, altura = self.fonte.size('')
        y = 0
        for num, i in enumerate(self.opcoes):
            texto_str = '> ' if self.sel == num else '  '
            texto_str += i

            texto = self.fonte.render(texto_str, 0, (255, 255, 255))
            canva.blit(texto, (0, y))
            y += altura

        return True

    def escape(self):
        return self.xadrez
