from .abc_movimento import MovimentoEspecial
from .util import tabuleiro_copia


def testar_xeque(tabuleiro: list[list], flags: list, pos_rei: tuple[int, int]) -> bool:
    """
    Testa se o rei está em xeque
    :param pos_rei: posição do rei
    """

    ri, rj = pos_rei
    rei = tabuleiro[ri][rj]
    for pi, linha in enumerate(tabuleiro):
        for pj, peca in enumerate(linha):
            if peca is not None and peca.cor != rei.cor:
                movimentos = peca.get_movimentos_simples(
                    tabuleiro,
                    flags,
                    (pi, pj)
                )
                if isinstance(movimentos[ri][rj], bool) and movimentos[ri][rj]:
                    return True
                elif isinstance(movimentos[ri][rj], MovimentoEspecial) and not movimentos[ri][rj].avanco:
                    return True
    return False


# TODO pode ser muito otimizado
def testar_movimento(tabuleiro: list[list], flags: list, pos_rei: tuple[int, int], acao: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    tab = tabuleiro_copia(tabuleiro)
    pos, nova_pos = acao
    i, j = pos
    m, n = nova_pos
    movimento = tab[i][j].get_movimentos_simples(tab, flags, pos)[m][n]

    # Movimenta peca
    if isinstance(movimento, bool) and movimento:
        tab[m][n] = tabuleiro[i][j]
        tab[i][j] = None
        tab[m][n].notifica_movimento()

        if pos_rei == pos:
            pos_rei = nova_pos

        flags.clear()

    elif isinstance(movimento, MovimentoEspecial):
        movimento.executar(tab, flags)

        if movimento.nome == 'roque' and pos_rei == movimento.rei:
            pos_rei = movimento.nova_rei

        flags.clear()
        movimento.update_flags(flags)
    else:
        return False

    # Testa Xeque
    return not testar_xeque(tab, flags, pos_rei)
