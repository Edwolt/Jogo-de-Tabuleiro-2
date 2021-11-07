import pygame
from pygame import display
from pygame import Surface
from pygame.event import Event
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_RETURN, K_ESCAPE

from glob import glob
from abc import ABC, abstractmethod
from typing import Optional, Union
from typing import Generator, NamedTuple

from recursos import Recursos
from tipos import load_gen, load_bar

from .abc_janela import Janela
from .loading import Loading


class Op(NamedTuple):
    """Guarda uma opcao de uma lista de opções"""
    sel: bool
    nome: str


Listagem = Generator[Op, None, None]


class Opcoes(ABC):
    def __init__(self, menu: 'Menu', anterior: 'Optional[Opcoes]'):
        """
        Classe abstrata para criar menus de opções
        A objeto armazena qual opção está armazenado nela e é capaz de executá-la
        :param menu: Objeto da classe Menu
        :param anterior: Opcoes anteriores
        """

        self.menu = menu
        self.anterior = anterior
        self.sel = 0
        self.opcoes: tuple[str, ...] = ()

    ##### Interface #####
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
        """:return: o nome da opção em key"""
        return self.opcoes[key]

    @abstractmethod
    def executar(self, key) -> 'Union[None, Opcoes, load_gen]':
        """
        Executa a opção de número key
        :return: Pode ser
        * None: Sair do menu
        * Opcoes: Qual novo menu de opções deve entrar
        * load_gen: Cria uma tela de Loading e sai do menu
        """

    def listar(self) -> Listagem:
        """
        :yield: (selecionado, nome)
        selecionado: se é aquela opção que está selecionada
        nome: nome da opção selecionada
        """

        yield from (Op(self.sel == i, self.nome(i)) for i in range(self.tamanho))

    def voltar(self):
        return self.anterior


class OpcoesConfigs(Opcoes):
    def __init__(self, menu: 'Menu', anterior: Opcoes):
        super().__init__(menu, anterior)
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
            recursos = Recursos()
            recursos.set_config(self.configs[self.sel])
            return recursos.carregar()
        else:
            return self.voltar()


class OpcoesPrincipal(Opcoes):
    def __init__(self, menu: 'Menu', anterior: Optional[Opcoes] = None):
        super().__init__(menu, anterior)
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
            return OpcoesConfigs(self.menu, self)
        elif opcao == 'novo jogo':
            self.menu.xadrez.__init__()
        elif opcao == 'sair':
            pygame.quit()
            quit(0)
        else:
            print(f'{opcao} não implementado')


class Menu(Janela):
    def __init__(self, xadrez, opcoes: Optional[Opcoes] = None):
        recursos = Recursos()
        self.xadrez = xadrez

        self.loading = None
        self.atualizacao = True
        self.finalizado = False
        self.fonte = recursos.config.fonte(50)

        if opcoes is None:
            self.opcoes: Opcoes = OpcoesPrincipal(self)
        else:
            self.opcoes = opcoes

    ##### Interface #####
    def event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                ret = self.opcoes.executar(self.opcoes.sel)

                if isinstance(ret, Opcoes):
                    self.opcoes = ret
                elif ret is None:
                    self.finalizado = True
                else:
                    self.loading = ret
            elif event.key == K_ESCAPE:
                ret = self.opcoes.voltar()
                if ret == None:
                    self.finalizado
                else:
                    self.opcoes = ret
            else:
                self.opcoes.event(event)
            self.atualizacao = True

    def draw(self, canvas: Surface) -> None:
        if not self.atualizacao:
            return
        if self.opcoes is None:
            return

        recursos = Recursos()
        recursos.config.menu_fundo(canvas)

        altura = self.fonte.size('')[1]
        y = 0
        for selecionado, nome in self.opcoes.listar():
            texto_str = ('> ' if selecionado else '  ') + nome
            texto = self.fonte.render(
                texto_str,
                False,
                recursos.config.menu_cor(selecionado)
            )
            canvas.blit(texto, (0, y))
            y += altura

        self.atualizacao = False
        display.set_caption('Menu')
        display.flip()

    def new(self):
        if self.finalizado:
            return self.xadrez
        elif self.loading is not None:
            return Loading(self.loading, self.xadrez)
        else:
            return self
