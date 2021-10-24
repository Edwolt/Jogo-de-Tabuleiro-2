import pygame
from pygame import display
from pygame import Surface
from pygame.event import Event
from pygame.locals import *

from glob import glob

from recursos import Recursos
from loading import Loading


class Opcoes:
    def __init__(self, menu, recursos: Recursos, anterior):
        """
        Classe abstrata para criar menus de opções
        A objeto armazena qual opção está armazenado nela e é capaz de executá-la
        :param menu: Objeto da classe Menu
        :param anterior: Opcoes anteriores
        """
        self.menu = menu
        self.anterior = anterior
        self.recursos = recursos
        self.sel = 0

    def event(self, event: Event) -> None:
        if event.key == K_UP:
            if self.sel > 0:
                self.sel -= 1
            else:
                self.sel = self.tamanho - 1
        elif event.key == K_DOWN:
            if self.sel < self.tamanho - 1:
                self.sel += 1
            else:
                self.sel = 0

    @property
    def tamanho(self) -> int:
        """:return: Número de opções"""
        return len(self.opcoes)

    def nome(self, key) -> str:
        """:return: o nome da opção de numero"""
        return self.opcoes[key]

    def executar(self, key):
        """
        Executa a opção de número key
        :return: Pode ser
        * None: Sair do menu
        * Opcoes: Qual novo menu de opções deve entrar
        * Generator: Cria uma tela de Loading e sai do menu
        """

        return self.voltar()

    def listar(self):
        """
        :yield: (selecionado, nome)
        selecionado: se é aquela opção que está selecionada
        nome: nome da opção selecionada
        """

        yield from ((self.sel == i, self.nome(i)) for i in range(self.tamanho))

    def voltar(self):
        return self.anterior


class OpcoesConfigs(Opcoes):
    def __init__(self, menu, recursos: Recursos, anterior: Opcoes):
        super().__init__(menu, recursos, anterior)
        self.configs = self.listar_configs()

    def listar_configs(self) -> list[str]:
        """Lista todas as configs na pasta Configs"""
        # 8 por causa do nome da pasta
        # -3 por causa da extensao
        return [i[8:-3] for i in glob('configs/*py')]

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
            return self.recursos.carregar()
        else:
            return self.voltar()


class OpcoesPrincipal(Opcoes):
    def __init__(self, menu,  recursos: Recursos, anterior: Opcoes = None):
        super().__init__(menu, recursos, anterior)
        self.opcoes = (
            'Config',
            'Imagens',
            'Fonte',
            'Desfazer',
            'Novo Jogo',
            'Voltar',
            'Sair'
        )

    ##### Interface #####
    def executar(self, i=None):
        i = self.sel if i is None else i
        opcao = self.nome(i).lower()
        if opcao == 'config':
            return OpcoesConfigs(self.menu, self.recursos, self)
        elif opcao == 'novo jogo':
            self.menu.xadrez.__init__(self.recursos)
        elif opcao == 'sair':
            pygame.quit()
            quit(0)
        else:
            print(f'{opcao} não implementado')


class Menu:
    def __init__(self, recursos: Recursos, xadrez, opcoes: Opcoes = None):
        self.recursos = recursos
        self.xadrez = xadrez

        self.loading = None
        self.atualizacao = True
        self.fonte = self.recursos.config.fonte(50)

        if opcoes is None:
            self.opcoes = OpcoesPrincipal(self, self.recursos)
        else:
            self.opcoes = opcoes

    ##### Interface #####
    def event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                ret = self.opcoes.executar(self.opcoes.sel)
                if isinstance(ret, Opcoes) or ret is None:
                    self.opcoes = ret
                else:
                    self.loading = ret
            elif event.key == K_ESCAPE:
                self.opcoes = self.opcoes.voltar()
            else:
                self.opcoes.event(event)
            self.atualizacao = True

    def draw(self, canvas: Surface) -> None:
        if not self.atualizacao:
            return
        if self.opcoes is None:
            return

        self.recursos.config.menu_fundo(canvas)

        altura = self.fonte.size('')[1]
        y = 0
        for selecionado, nome in self.opcoes.listar():
            texto_str = ('> ' if selecionado else '  ') + nome
            texto = self.fonte.render(
                texto_str,
                0,
                self.recursos.config.menu_cor(selecionado)
            )
            canvas.blit(texto, (0, y))
            y += altura

        self.atualizacao = False
        display.set_caption('Menu')
        display.flip()

    def new(self):
        if self.opcoes is None:
            return self.xadrez
        elif self.loading is not None:
            return Loading(self.recursos, self.loading, self.xadrez)
        else:
            return self
