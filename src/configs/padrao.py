from pygame import Surface


class Config:
    def __init__(self):
        self.vazio = (
            (255, 255, 255),  # Branco
            (0, 0, 0)  # Preto
        )
        self.click = 255, 0, 0
        self.movimento = 0, 255, 255
        self.background = 0, 0, 0
        self.foreground = 255, 255, 255

    def quadrado(self, canva: Surface, pos: tuple, tipo: str, complemento=None):
        i, j = pos

        cor = 0, 0, 0
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento

        canva.fill(cor)

    def menu_fundo(self, canva: Surface) -> None:
        canva.fill(self.background)

    def menu_cor(self, texto: str, selecionado: bool) -> tuple:
        return self.foreground

    def titulo(self, vez: bool) -> str:
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')
