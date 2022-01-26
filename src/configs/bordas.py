from __future__ import annotations

import pygame as pg

import tipos as tp


class ConfigBordas:
    def __init__(self):
        self.vazio = tp.pb(pg.Color(124, 49, 0), pg.Color(214, 165, 132))
        self.click = pg.Color(153, 0, 0)
        self.movimento = pg.Color(229, 126, 0)
        self.xeque = pg.Color(100, 0, 0)
        self.borda = pg.Color(100, 100, 100)
        self.background = pg.Color(0, 0, 0)
        self.foreground = pg.Color(255, 255, 255)
        self.selecionado = pg.Color(255, 0, 0)

    def quadrado(self, canvas: pg.Surface, pos: tp.coord, tipo: str) -> None:
        size = canvas.get_size()
        quad = pg.Rect(1, 1, size[0] - 2, size[1] - 2)

        canvas.fill(self.borda)

        i, j = pos

        match tipo:
            case "vazio":
                cor = self.vazio[(i + j) % 2 == 0]
            case "click":
                cor = self.click
            case "movimento":
                cor = self.movimento
            case "especial":
                cor = self.movimento
            case "captura":
                cor = self.movimento
            case "xeque":
                pg.draw.rect(canvas, self.vazio[(i + j) % 2 == 0], quad)
                pg.draw.circle(
                    canvas,
                    self.xeque,
                    (canvas.get_size()[0] / 2, canvas.get_size()[0] / 2),
                    min(*canvas.get_size()) / 3,
                )
                return
            case _:
                cor = pg.Color(0, 0, 0)

        pg.draw.rect(canvas, cor, quad)

    def pecas_cor(self) -> tp.pb[tp.grad]:
        return tp.pb(
            tp.grad(pg.Color(0, 0, 0, 0), pg.Color(100, 100, 100, 255)),
            tp.grad(pg.Color(100, 100, 100, 0), pg.Color(255, 255, 255, 255)),
        )

    def menu_fundo(self, canvas: pg.Surface) -> None:
        canvas.fill(self.background)

    def menu_opcao(self, opcao: str, selecionado: bool) -> tuple[str, pg.Color]:
        if selecionado:
            return "> " + opcao, self.selecionado
        else:
            return "  " + opcao, self.foreground

    def loading_cores(self) -> tuple[pg.Color, pg.Color]:
        return pg.Color(0, 255, 0), pg.Color(255, 0, 0)

    def titulo(self, vez: bool) -> str:
        texto_cor = tp.pb("Preto", "Braco")
        return "Xadrez : " + texto_cor[vez]

    def fonte(self, tam) -> pg.font.Font:
        return pg.font.Font(
            "assets/inconsolata/static/Inconsolata-Medium.ttf", tam
        )


export = ConfigBordas
