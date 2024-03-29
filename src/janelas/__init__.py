from __future__ import annotations

__all__ = ["Janela", "Escolha", "Loading", "Menu", "Xadrez"]  # ABC  # Janelas

# ABC
from .abc_janela import Janela

# Janelas
from .escolha import Escolha
from .loading import Loading
from .menu import Menu
from .xadrez import Xadrez
