
from __future__ import annotations

import pygame as pg
from dataclasses import dataclass, astuple
from typing import Optional, Generator
from typing import Generic, TypeVar
from typing import NewType, NamedTuple

from pecas import Peca, Movimento


board = NewType('board', list[list[Optional[Peca]]])
"""
Matriz board que representa as peças no tabuleiro
Se o espaço estiver vazio o valor será None
"""


movements = NewType('movements', list[list[Optional[Movimento]]])
"""
Matriz movements que representa todos os movimentos que são possível para
aquela peça
Se o movimento não for possível o valor naquela posição será None
"""


class load_bar(NamedTuple):
    """
    Representa quanto falta para concluir uma tarefa para permitir desenhar uma
    barra de carregamento
    tam: O total de tarefas a ser feita, incluindo as que já foram concluídas
    val: O quanto já foi feito
    """

    tam: int
    val: int


load_gen = Generator[list[load_bar], None, None]
"""Generator de load_bar"""


T = TypeVar('T')


@dataclass
class pb(Generic[T]):
    """
    Armazena um valor para as pretas e o brancas

    Pode ser indexado com um valor bool
    """

    # Isso faz funcionar como o NamedTuple
    __slots__ = ('preto', 'branco')

    preto: T
    branco: T

    def __getitem__(self, index: bool) -> T:
        return self.branco if index else self.preto

    def __setitem__(self, index: bool, valor: T):
        if index:
            self.branco = valor
        else:
            self.preto = valor

    # Isso faz funcionar como o NamedTuple
    def __iter__(self):
        yield from astuple(self)


class grad(NamedTuple):
    """Representa um gradiente de cor com um valor inicial e um final"""

    start: pg.Color
    end: pg.Color

    def gerar_cor(self, c: pg.Color) -> pg.Color:
        """:return: A cor equivalente a c dentro do gradiente"""
        res = pg.Color(0, 0, 0)
        a, b = self
        for k in range(len(res)):
            res[k] = int(a[k] + (b[k] - a[k]) * (c[k] / 255))
        return res

    def transparencia_padrao(self):
        """Configura a transparência para variar de 0 a 255"""
        self.start.a = 0
        self.end.a = 255


class direction(NamedTuple):
    i: int
    j: int


class coord(NamedTuple):
    """Um coordenada dentro do tabuleiro"""

    i: int
    j: int

    @staticmethod
    def valida_componente(val: int):
        """Verifica se a é um valor válido para componente de uma coordenada"""
        return 0 <= val < 8

    def valida(self) -> bool:
        """Verifica se é uma coordenada válida"""
        return 0 <= self.i < 8 and 0 <= self.j < 8


class action(NamedTuple):
    """Um movimento a ser feito"""

    pos: coord
    nova_pos: coord


class pathaction(NamedTuple):
    """Um movimento a ser feito e uma coordenada pelo qual a peça passou"""

    pos: coord
    meio: coord
    nova_pos: coord

    def to_action(self) -> action:
        return action(self.pos, self.nova_pos)
