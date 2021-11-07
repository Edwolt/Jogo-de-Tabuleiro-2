from pygame import Color

from dataclasses import dataclass, astuple
from typing import Generic, TypeVar, Union, overload
from typing import Optional, Generator, NamedTuple

from pecas import Peca, Movimento


T = TypeVar('T')


board = list[list[Optional[Peca]]]


movements = list[list[Optional[Movimento]]]


class load_bar(NamedTuple):
    tam: int
    val: int


load_gen = Generator[list[load_bar], None, None]


@dataclass
class pb(Generic[T]):
    # Isso faz funcionar como o NamedTuple
    __slots__ = ('preto', 'branco')

    preto: T
    branco: T

    def __getitem__(self, index: bool) -> T:
        return self.branco if index else self.preto

    # Isso faz funcionar como o NamedTuple
    def __iter__(self):
        yield from astuple(self)


class grad(NamedTuple):
    start: Color
    end: Color

    def gerar_cor(self, c: Color) -> Color:
        res = Color(0, 0, 0)
        a, b = self
        for k in range(len(res)):
            res[k] = int(a[k] + (b[k] - a[k]) * (c[k] / 255))
        return res

    def tranparencia_padrao(self):
        """ Configura a transparência para variar de 0 a 255 """
        self.start.a = 0
        self.end.a = 255


class direction(NamedTuple):
    i: int
    j: int


class coord(NamedTuple):
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
    pos: coord
    nova_pos: coord


class pathaction(NamedTuple):
    pos: coord
    meio: coord
    nova_pos: coord

    def to_action(self) -> action:
        return action(self.pos, self.nova_pos)
