from .abc_peca import Peca
from .abc_movimento import Movimento, MovimentoEspecial

from .rei import Rei, Roque
from .rainha import Rainha
from .bispo import Bispo
from .cavalo import Cavalo
from .torre import Torre
from .peao import Peao, Promocao, Avanco, AvancoDuplo, EnPassant

from .xeque import testar_xeque

LISTA_PECAS = [Rei, Rainha, Bispo, Cavalo, Torre, Peao]
LISTA_NOME_PECAS = ['rei', 'rainha', 'bispo', 'cavalo', 'torre', 'peao']
LISTA_MOVIMENTOS_ESPECIAIS = [Roque, Promocao, Avanco, AvancoDuplo, EnPassant]
LISTA_NOME_MOVIMENTOS_ESPECIAIS = [
    'roque', 'promocao', 'avanco', 'avancoDuplo', 'enpassant']
