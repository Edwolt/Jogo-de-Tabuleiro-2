class Config:
    def __init__(self):
        self.vazio = (
            (214, 165, 132),
            (124, 49, 0)
        )
        self.click = (153, 0, 0)
        self.movimento = (229, 126, 0)
        # 'menu': (214, 165, 132),
        # 'cor_fonte': (124, 49, 0)

    def quadrado(self, pos: tuple, tipo: str, complemento=None) -> None:
        x, y = pos
        if tipo == 'vazio':
            return self.vazio[(x+y) % 2]
        elif tipo == 'click':
            return self.click
        elif tipo == 'movimento':
            return self.movimento
        elif tipo == 'captura':
            return self.movimento
        else:
            return (0, 0, 0)

    def titulo(self, vez: bool) -> None:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')

    # 'menu': lambda cores, menu: self.cores['menu'],
    # 'cor_fonte': lambda cores, menu: self.cores['cor_fonte']
