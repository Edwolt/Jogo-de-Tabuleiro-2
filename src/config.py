import importlib


def Config(nome: str):
    return importlib.import_module(f'configs.{nome}').Config()
