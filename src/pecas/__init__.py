from __future__ import annotations

__all__ = [
    'Peca', 'Movimento', 'MovimentoEspecial',  # ABC
    'Rei', 'Rainha', 'Bispo', 'Cavalo', 'Torre', 'Peao',  # Pecas
    'Roque', 'Promocao', 'Avanco', 'AvancoDuplo', 'EnPassant',  # Movimentos
    'testar_xeque',  # Funções
]

# ABC
from .abc_peca import Peca
from .abc_movimento import Movimento, MovimentoEspecial

# Pecas
from .rei import Rei
from .rainha import Rainha
from .bispo import Bispo
from .cavalo import Cavalo
from .torre import Torre
from .peao import Peao

# Movimentos
from .rei import Roque
from .peao import Promocao, Avanco, AvancoDuplo, EnPassant

# Funções
from .xeque import testar_xeque


# Listas
LISTA_PECAS = [
    Rei,
    Rainha,
    Bispo,
    Cavalo,
    Torre,
    Peao
]

LISTA_NOME_PECAS = [
    'rei',
    'rainha',
    'bispo',
    'cavalo',
    'torre',
    'peao'
]

LISTA_MOVIMENTOS_ESPECIAIS = [
    Roque,
    Promocao,
    Avanco,
    AvancoDuplo,
    EnPassant
]

LISTA_NOME_MOVIMENTOS_ESPECIAIS = [
    'roque',
    'promocao',
    'avanco',
    'avancoDuplo',
    'enpassant'
]
