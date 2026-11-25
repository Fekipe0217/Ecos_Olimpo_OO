from rpg_core.entities.entity import Entity
from rpg_core.items.inventory_item import InventoryItem


_ITEM_CATALOG: dict[str, tuple[str, str]] = {
    "Néctar": ("Bebida divina dos deuses que restaura 35 de HP.", "heal"),
    "Ambrosia": ("Alimento sagrado que restaura 60 de HP e 20 de Energia.", "hybrid"),
    "Elixir Olímpico": ("Restaura 35 pontos de Energia em combate.", "energy"),
}


class Inventory:
    """Gerencia o inventário do semideus, compondo objetos InventoryItem."""

    def __init__(self) -> None:
        # COMPOSIÇÃO: Inventory cria e controla o ciclo de vida dos objetos InventoryItem
        self._items: dict[str, InventoryItem] = {}

    def addItem(self, name: str, count: int) -> None:
        """Adiciona uma quantidade de um item ao inventário, criando o InventoryItem se necessário."""
        if count <= 0:
            return

        if name in self._items:
            self._items[name].count += count
        else:
            description, item_type = _ITEM_CATALOG.get(
                name, ("Item consumível que restaura 25 de HP.", "heal")
            )
            self._items[name] = InventoryItem(
                name=name,
                description=description,
                count=count,
                itemType=item_type,
            )

    # DEPENDÊNCIA: useItem() recebe Entity para aplicar os efeitos do item no usuário
    def useItem(self, name: str, user: Entity) -> bool:
        """Consome 1 unidade do item e aplica seu efeito no usuário."""
        item = self._items.get(name)
        if item is None or item.count <= 0:
            return False

        if item.itemType == "heal":
            heal_amount = 35 if item.name == "Néctar" else 25
            user.heal(heal_amount)
        elif item.itemType == "energy":
            user.restoreEnergy(35)
        elif item.itemType == "hybrid":
            user.heal(60)
            user.restoreEnergy(20)

        item.count -= 1
        if item.count <= 0:
            del self._items[name]
        return True

    def getItems(self) -> list[InventoryItem]:
        """Retorna a lista de itens atualmente disponíveis no inventário."""
        return list(self._items.values())
