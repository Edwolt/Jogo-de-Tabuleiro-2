import importlib


def Config(nome: str):
    return importlib.import_module(f'configs.{nome}').Config()


class Recursos:
    def __init__(self, config, size=(800, 800), framerate=60):
        self.config = Config(config)
        self.size = size
        self.framerate = framerate

    def carregar(self):
        pass
