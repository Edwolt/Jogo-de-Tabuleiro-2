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

    def quadrado(self, size, pos: tuple, tipo: str, complemento=None) -> Surface:
        surf = Surface((size[0], size[1]))
        quad = Surface((size[0] - 2, size[1] - 2))

        surf.fill((50, 50, 50))

        x, y = pos

        color = (0, 0, 0)
        if tipo == 'vazio':
            color = self.vazio[(x+y) % 2]
        elif tipo == 'click':
            color = self.click
        elif tipo == 'movimento':
            color = self.movimento
        elif tipo == 'captura':
            color = self.movimento

        quad.fill(color)
        surf.blit(quad, (1, 1))
        return surf

    def titulo(self, vez: bool) -> None:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')

    # 'menu': lambda cores, menu: self.cores['menu'],
    # 'cor_fonte': lambda cores, menu: self.cores['cor_fonte']
