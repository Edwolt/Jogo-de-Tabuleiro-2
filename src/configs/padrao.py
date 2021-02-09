from pygame import Color, Surface
from pygame.font import Font


class Config:
    def __init__(self):
        self.vazio = (
            Color(255, 255, 255),  # Branco
            Color(0, 0, 0)  # Preto
        )
        self.click = Color(255, 255, 0)
        self.movimento = Color(0, 255, 255)
        self.xeque = Color(255, 0, 0)
        self.background = Color(0, 0, 0)
        self.foreground = Color(255, 255, 255)

    def quadrado(self, canva: Surface, pos: tuple[int, int], tipo: str, complemento=None) -> None:
        """
        Colore o quadrado que será usado em baixo da peça
        :param pos: Posição da peça
        :param tipo: Se tem algo especial no quadrado
        * vazio: Um quadrado comun, pode estar ou não vazio
        * click: Último quadrado que foi clicado
        * movimento: Quadrado disponível para movimentar
        * captura: Quadrado disponível para movimentar que reultará em um captura
        :param complemento: (ainda não tem nenhuma função, mas a ideia é usar para salvar mais detalhes sobre o quadrado)
        """

        i, j = pos

        cor = Color(0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento
        elif tipo == 'xeque':
            cor = self.xeque

        canva.fill(cor)

    def menu_fundo(self, canva: Surface) -> None:
        """Colore o fundo do menu (canva)"""
        canva.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        """
        :param texto: Texto da opção
        :param selecionado: Se a opção está selecionada
        :return: Cor que será usada na fonte para desenhar essa opção
        """
        return self.foreground

    def loading_cores(self) -> tuple[Color, Color]:
        """[summary]
        :returns: Retorna uma tupla de cores para desenhar as barras de loading
        A primeira cor é usada para mostrar o que já foi carregado
        e a segunda o quanto falta
        """
        return Color(0, 255, 0), Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        """
        :param vez: Qual turno o jogo está
        :return: O título que será usado para a janela
        """
        return 'Xadrez : ' + ('Branco' if vez else 'Preto')

    def fonte(self, tam) -> Font:
        """
        :param tam: Tamanho da fonte
        :return: Objeto fonte
        """
        return Font(
            'assets/inconsolata/static/Inconsolata-Medium.ttf',
            tam
        )
