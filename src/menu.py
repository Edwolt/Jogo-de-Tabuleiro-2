import pygame
from pygame.font import Font
from pygame import Surface
from pygame.event import Event
from pygame.locals import *


class Menu:
    def __init__(self, xadrez, config):
        self.xadrez = xadrez
        self.config = config

        self.escape = False
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
                self.atualizacao = True
                if self.sel > 0:
                    self.sel -= 1
                else:
                    self.sel = len(self.opcoes) - 1

            elif event.key == K_DOWN:
                self.atualizacao = True
                if self.sel < len(self.opcoes) - 1:
                    self.sel += 1
                else:
                    self.sel = 0

            elif event.key == K_RETURN:
                self.atualizacao = True
                opcao = self.opcoes[self.sel].lower()
                if opcao == 'sair':
                    pygame.quit()
                    quit(0)
                else:
                    print(f'{self.opcoes[self.sel]} não implementado')
                    self.escape = True

            elif event.key == K_ESCAPE:
                self.escape = True

    def draw(self, canva: Surface):
        if not self.atualizacao:
            return False

        self.config.menu_fundo(canva)

        altura = self.fonte.size('')[1]
        y = 0
        for num, i in enumerate(self.opcoes):
            texto_str = '> ' if self.sel == num else '  '
            texto_str += i

            texto = self.fonte.render(
                texto_str,
                0,
                self.config.menu_cor(texto_str, self.sel == num)
            )
            canva.blit(texto, (0, y))
            y += altura

        self.atualizacao = False
        return True

    def new(self):
        if self.escape:
            self.escape = False
            return self.xadrez
        else:
            return None
