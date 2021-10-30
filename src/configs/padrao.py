from pygame import Color, Surface
from pygame.font import Font

from abc_config import Config


class ConfigPadrao(Config):
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

    def quadrado(self, canvas: Surface, pos: tuple[int, int], tipo: str) -> None:
        """
        Colore o quadrado que será usado em baixo da peça
        :param pos: Posição da peça
        :param tipo: Se tem algo especial no quadrado
        * vazio: Quadrado comum (pode estar ou não vazio)
        * click: Último quadrado que foi clicado
        * movimento: Quadrado disponível para movimentar
        * especial: Quadrado onde o movimento é especial
        * captura: Quadrado disponível para movimentar que resultará em um captura
        * xeque: Quadrado onde o rei está em xeque
        """

        i, j = pos

        cor = Color(0, 0, 0)
        if tipo == 'vazio':
            cor = self.vazio[(i+j) % 2]
        elif tipo == 'click':
            cor = self.click
        elif tipo == 'movimento':
            cor = self.movimento
        elif tipo == 'especial':
            cor = self.movimento
        elif tipo == 'captura':
            cor = self.movimento
        elif tipo == 'xeque':
            cor = self.xeque

        canvas.fill(cor)

    def pecas_cor(self) -> tuple[tuple[Color, Color], tuple[Color, Color]]:
        """
        :return: (gradiente_branco, gradiente_preto)
        Retorna dois gradientes, um para colorir as peças brancas outro para as peças pretas
        """
        return (
            (Color(0, 0, 0, 0), Color(100, 100, 100, 255)),
            (Color(100, 100, 100, 0), Color(255, 255, 255, 255))
        )

    def menu_fundo(self, canvas: Surface) -> None:
        """Colore o fundo do menu (canvas)"""
        canvas.fill(self.background)

    def menu_cor(self, selecionado: bool) -> Color:
        """
        :param texto: Texto da opção
        :param selecionado: Se a opção está selecionada
        :return: Cor que será usada na fonte para desenhar essa opção
        """
        return self.foreground

    def loading_cores(self) -> tuple[Color, Color]:
        """
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


export = ConfigPadrao
