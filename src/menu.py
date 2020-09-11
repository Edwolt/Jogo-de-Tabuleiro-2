from pygame.font import Font
from pygame import Surface
from pygame.event import Event


class Menu:
    def __init__(self, xadrez):
        self.xadrez = xadrez
        self.opcoes = [
            'Config',
            'Imagens',
            'Fonte',
            'Desfazer',
            'Voltar',
            'Sair'
        ]
        self.fonte = Font('assets/noto_sans/NotoSansTC-Medium.otf', 50)

    def carregar(self):
        return

    def event(self, event: Event):
        pass

    def draw(self, canva: Surface):
        canva.fill((0, 0, 0))

        _, altura = self.fonte.size('')
        y = 0
        for i in self.opcoes:
            texto = self.fonte.render(f'> {i}', 0, (255, 255, 255))
            canva.blit(texto, (0, y))
            y += altura

        return True

    def escape(self):
        return self.xadrez
