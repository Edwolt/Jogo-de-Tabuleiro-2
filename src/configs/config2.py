from pygame import Surface


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

    def quadrado(self, canva: Surface, pos: tuple, tipo: str, complemento=None) -> None:
        size = canva.get_size()
        quad = Surface((size[0] - 2, size[1] - 2))

        canva.fill((100, 100, 100))

        x, y = pos

        cor = (0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(x+y) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento

        quad.fill(cor)
        canva.blit(quad, (1, 1))

    def menu_fundo(self, canva: Surface) -> None:
        canva.fill((0, 0, 0))

    def menu_cor(self, texto: str, selecionado: bool) -> tuple:
        return (255, 255, 255)

    def titulo(self, vez: bool) -> None:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')

    # 'menu': lambda cores, menu: self.cores['menu'],
    # 'cor_fonte': lambda cores, menu: self.cores['cor_fonte']
