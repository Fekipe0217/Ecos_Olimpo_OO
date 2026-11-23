from rpg_core.entities.entity import Entity


class Inventory:
    """Gerencia os itens pertencentes a uma entidade (composto dentro de Demigod)."""

    def __init__(self) -> None:
        self._items: dict[str, int] = {}

    def addItem(self, name: str, count: int = 1) -> None:
        """Adiciona uma quantidade de um item ao inventário."""
        if count <= 0:
            return
        self._items[name] = self._items.get(name, 0) + count

    # DEPENDÊNCIA: useItem() recebe Entity para aplicar o efeito do item no usuário
    def useItem(self, name: str, user: Entity) -> bool:
        """Consome uma unidade do item se disponível e aplica seu efeito básico."""
        if self._items.get(name, 0) <= 0:
            return False
        self._items[name] -= 1
        if self._items[name] == 0:
            del self._items[name]
        # No MVP da Etapa 0.1, itens restauram HP diretamente de forma simples
        user._current_hp = min(user.getMaxHp(), user.getCurrentHp() + 25)
        return True

    def getItems(self) -> dict[str, int]:
        return dict(self._items)
