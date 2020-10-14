import pygame
from pygame import display
from pygame import Surface
from pygame.event import Event
from pygame.font import Font
from pygame.locals import *

from glob import glob

from recursos import Recursos


class Submenu:
    """
    Classe abstrata para criar menus de opções
    A objeto armazena qual opção está armazenado nela e é capaz de executá-la
    """

    def __init__(self, recursos: Recursos):
        self.recursos = recursos
        self.sel = 0

    @property
    def tamanho(self) -> int:
        """
        :return: Número de opções
        """
        return len(self.opcoes)

    def nome(self, key) -> str:
        """Retorna o neme da opção de numero"""
        return self.opcoes[key]

    def executar(self, key):
        """Executa a opção de número key"""
        self.funcoes[key]()

    def subir(self):
        """Muda o seletor para a opção de cima"""
        if self.sel > 0:
            self.sel -= 1
        else:
            self.sel = self.opcoes.tamanho - 1

    def descer(self):
        """Muda o seletor para a opção de baixo"""
        if self.sel < self.tamanho - 1:
            self.sel += 1
        else:
            self.sel = 0

    def listar(self):
        """
        :yield: (selecionado, nome)
        selecionado: se é aquela opção que está selecionada
        nome: nome da opção selecionada
        """
        for i in range(self.tamanho):
            yield self.sel == i, self.nome(i)

    def voltar(self):
        return self.anterior


class MenuConfigs(Submenu):
    def __init__(self, recursos: Recursos, anterior):
        super().__init__(recursos)
        self.anterior = anterior
        self.configs = list(self.listar_configs())

    def listar_configs(self):
        """
        :yield: [description]
        :rtype: Iterator[list]
        """
        # 8 por causa do nome da pasta
        # -3 por causa da extensao
        for i in glob('configs/*py'):
            yield i[8:-3]

    ##### Interface #####
    @property
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
    def __init__(self, recursos: Recursos):
        super().__init__(recursos)
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
            return MenuConfigs(self.recursos, self)
        elif opcao == 'sair':
            pygame.quit()
            quit(0)
        else:
            print(f'{opcao} não implementado')

    def voltar(self):
        return None


class Menu:
    def __init__(self, recursos: Recursos, xadrez, opcoes: Submenu = None):
        self.recursos = recursos
        self.xadrez = xadrez

        self.atualizacao = True
        self.fonte = Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            50
        )

        if opcoes is None:
            self.opcoes = MenuPrincipal(self.recursos)
        else:
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
