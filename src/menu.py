import pygame
from pygame import display
from pygame import Surface
from pygame.event import Event
from pygame.font import Font
from pygame.locals import *

from glob import glob

from recursos import Recursos


class Submenu:
    def __init__(self):
        self.sel = 0

    def tamanho(self) -> int:
        return len(self.opcoes)

    def nome(self, key) -> str:
        return self.opcoes[key]

    def executar(self, key):
        self.funcoes[key]()

    def subir(self):
        if self.sel > 0:
            self.sel -= 1
        else:
            self.sel = self.opcoes.tamanho() - 1

    def descer(self):
        if self.sel < self.tamanho() - 1:
            self.sel += 1
        else:
            self.sel = 0

    def listar(self) -> tuple:
        for i in range(self.tamanho()):
            yield self.sel == i, self.nome(i)

    def voltar(self):
        return self.anterior


class MenuConfigs(Submenu):
    def __init__(self, anterior):
        super().__init__()
        self.anterior = anterior
        self.configs = self.listar_configs()

    def listar_configs(self) -> list:
        # 8 por causa do nome da pasta
        # -3 por causa da extensao
        return [i[8:-3] for i in glob('configs/*py')]

    ##### Interface #####
    def tamanho(self) -> int:
        return len(self.configs) + 1

    def nome(self, i) -> str:
        if 0 <= i < len(self.configs):
            return self.configs[i]
        else:
            return 'Voltar'

    def executar(self, i):
        if 0 <= i < len(self.configs):
            self.recursos.set_config(self.configs[self.sel])
        else:
            return self.voltar()


class MenuPrincipal(Submenu):
    def __init__(self):
        super().__init__()
        self.opcoes = (
            'Config',
            'Imagens',
            'Fonte',
            'Desfazer',
            'Voltar',
            'Sair'
        )

    ##### Interface #####
    def executar(self, i=None):
        i = self.sel if i is None else i
        opcao = self.nome(i).lower()
        if opcao == 'config':
            return MenuConfigs(self)
        elif opcao == 'sair':
            pygame.quit()
            quit(0)
        else:
            print(f'{opcao} não implementado')

    def voltar(self):
        return None


class Menu:
    def __init__(self, xadrez, recursos: Recursos, opcoes: Submenu = MenuPrincipal()):
        self.xadrez = xadrez
        self.recursos = recursos

        self.enter = None
        self.atualizacao = True

        self.fonte = Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            50
        )
        self.opcoes = opcoes

    ##### Interface #####
    def event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.opcoes.subir()
            elif event.key == K_DOWN:
                self.opcoes.descer()
            elif event.key == K_RETURN:
                self.opcoes = self.opcoes.executar(self.opcoes.sel)
            elif event.key == K_ESCAPE:
                self.opcoes = self.opcoes.voltar()
            self.atualizacao = True

    def draw(self, canva: Surface) -> None:
        if not self.atualizacao:
            return
        if self.opcoes is None:
            return

        self.recursos.config.menu_fundo(canva)

        altura = self.fonte.size('')[1]
        y = 0
        for selecionado, nome in self.opcoes.listar():
            texto_str = ('> ' if selecionado else '  ') + nome
            texto = self.fonte.render(
                texto_str,
                0,
                self.recursos.config.menu_cor(texto_str, selecionado)
            )
            canva.blit(texto, (0, y))
            y += altura

        self.atualizacao = False
        display.set_caption('Menu')
        display.flip()

    def new(self):
        if self.opcoes is None:
            return self.xadrez
        else:
            return self
