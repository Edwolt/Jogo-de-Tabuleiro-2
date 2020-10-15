import importlib


def Config(nome: str):
    return importlib.import_module(f'configs.{nome}').Config()


# TODO carregar todas as imagens aqui
class Recursos:
    def __init__(self, config: str, size: tuple = (800, 800), framerate: int = 60):
        self.config = Config(config)
        self.size = size
        self.framerate = framerate

    def set_config(self, config: str) -> None:
        self.config = Config(config)

    def carregar(self):
        ...
