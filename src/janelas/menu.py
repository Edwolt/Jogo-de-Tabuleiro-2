from __future__ import annotations

import pygame as pg
from typing import Generator, NamedTuple
from typing import Optional, Union
from abc import ABC, abstractmethod
from glob import glob

import tipos as tp
from recursos import Recursos

from .abc_janela import Janela
from .loading import Loading


class Op(NamedTuple):
    """
    Guarda uma opcao de uma lista de opções
    sel: se é aquela opção que está selecionada
    nome: nome da opção selecionada
    """
    sel: bool
    nome: str


Listagem = Generator[Op, None, None]


class Opcoes(ABC):
    def __init__(self, menu: Menu, anterior: Optional[Opcoes]):
        """
        Classe abstrata para criar menus de opções
        A objeto armazena qual opção está armazenado nela e é capaz de executá-la
        :param menu: Objeto da classe Menu
        :param anterior: Objeto Opcoes que estava sendo exibida anteriormente e
        portanto é para onde deve voltar
        """
        self.menu = menu
        self.anterior = anterior
        self.sel = 0
        self.opcoes: tuple[str, ...] = tuple()

    ##### Interface #####
    def event(self, event: pg.event.Event) -> None:
        if event.key == pg.K_UP:
            if self.sel > 0:
                self.sel -= 1
            else:
                self.sel = self.tamanho - 1
        elif event.key == pg.K_DOWN:
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
    def executar(self, key) -> Union[None, Opcoes, tp.load_gen]:
        """
        Executa a opção de número key
        :return: Pode ser
        * None: Sair do menu
        * Opcoes: Qual novo menu de opções deve entrar
        * load_gen: Cria uma tela de Loading e sai do menu
        """

    def listar(self) -> Listagem:
        """:yield: Op(selecionado, nome)"""
        yield from (
            Op(self.sel == i, self.nome(i))
            for i in range(self.tamanho)
        )

    def voltar(self):
        return self.anterior


class OpcoesConfigs(Opcoes):
    def __init__(self, menu: Menu, anterior: Opcoes):
        super().__init__(menu, anterior)
        self.configs = self._listar_configs()

    def _listar_configs(self) -> list[str]:
        """Lista todas as configs na pasta Configs"""
        PASTA = 'configs'
        EXT = '.py'
        BUSCA = f'{PASTA}/*{EXT}'  # configs/*.py

        return [i[len(PASTA+'/'): -len(EXT)] for i in glob(BUSCA)]

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
    def __init__(self, menu: Menu, anterior: Optional[Opcoes] = None):
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
            pg.quit()
            quit(0)
        else:
            print(f'{opcao} não implementado')


class Menu(Janela):
    def __init__(self, xadrez, opcoes: Optional[Opcoes] = None):
        recursos = Recursos()
        self.xadrez = xadrez

        self._loading = None
        self._atualizacao = True
        self._finalizado = False

        self.fonte = recursos.config.fonte(50)

        if opcoes is None:
            self.opcoes: Opcoes = OpcoesPrincipal(self)
        else:
            self.opcoes = opcoes

    ##### Interface #####
    def event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                ret = self.opcoes.executar(self.opcoes.sel)

                if isinstance(ret, Opcoes):
                    self.opcoes = ret
                elif ret is None:
                    self._finalizado = True
                else:  # isinstance(ret, load_gen)
                    self._loading = ret
            elif event.key == pg.K_ESCAPE:
                ret = self.opcoes.voltar()
                if ret == None:
                    self._finalizado
                else:
                    self.opcoes = ret
            else:
                self.opcoes.event(event)
            self._atualizacao = True

    def draw(self, canvas: pg.Surface) -> None:
        if not self._atualizacao:
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

        self._atualizacao = False
        pg.display.set_caption('Menu')
        pg.display.flip()

    def new(self):
        if self._finalizado:
            return self.xadrez
        elif self._loading is not None:
            return Loading(self._loading, self.xadrez)
        else:
            return self
