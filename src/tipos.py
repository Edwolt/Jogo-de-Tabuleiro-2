from pygame import Color

from typing import Optional, NamedTuple

from pecas import Peca, Movimento


matriz_tabuleiro = list[list[Optional[Peca]]]


matriz_movimento = list[list[Optional[Movimento]]]


grad = tuple[Color, Color]


direction = tuple[int, int]


class coord(NamedTuple):
    i: int
    j: int


class mov(NamedTuple):  # TODO pode ser chamado de acao
    pos: coord
    nova_pos: coord
