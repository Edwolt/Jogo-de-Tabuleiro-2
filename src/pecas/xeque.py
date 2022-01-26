from __future__ import annotations

import tipos as tp

from .abc_movimento import Movimento, MovimentoComplexo
from .util import board_copia


def testar_xeque(tabuleiro: tp.board, flags: list, pos_rei: tp.coord) -> bool:
    """
    Testa se o rei está em xeque
    :param pos_rei: posição do rei
    """
    from .rei import Rei  # TODO resolve the circular import

    ri, rj = pos_rei
    rei = tabuleiro[ri][rj]
    if rei is None or not isinstance(rei, Rei):
        raise Exception(
            "testar_xeque não recebeu uma posição válida para o rei"
        )

    for pi, linha in enumerate(tabuleiro):
        for pj, peca in enumerate(linha):
            if peca is not None and peca.cor != rei.cor:
                movimentos = peca.get_movimentos_simples(
                    tabuleiro, flags, tp.coord(pi, pj)
                )
                mov = movimentos[ri][rj]
                if isinstance(mov, Movimento):
                    return True
                elif isinstance(mov, MovimentoComplexo) and not mov.avanco:
                    return True
    return False


# TODO pode ser muito otimizado
def testar_movimento(
    tabuleiro: tp.board, flags: list, pos_rei: tp.coord, acao: tp.action
) -> bool:
    from .rei import Roque

    tab = board_copia(tabuleiro)
    pos, nova_pos = acao
    i, j = pos
    m, n = nova_pos

    peca = tab[i][j]
    if peca is None:
        return False

    movimento = peca.get_movimentos_simples(tab, flags, pos)[m][n]

    # Movimenta peca
    if isinstance(movimento, bool) and movimento:
        tab[m][n] = tabuleiro[i][j]
        tab[i][j] = None

        peca = tab[m][n]
        peca is None or peca.notifica_movimento()

        if pos_rei == pos:
            pos_rei = nova_pos

        flags.clear()

    elif isinstance(movimento, MovimentoComplexo):
        movimento.executar(tab, flags)

        if isinstance(movimento, Roque) and pos_rei == movimento.rei:
            pos_rei = movimento.acao_rei.nova_pos

        flags.clear()
        movimento.atualiza_flags(flags)
    else:
        return False

    # Testa Xeque
    return not testar_xeque(tab, flags, pos_rei)
