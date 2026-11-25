from dataclasses import dataclass


@dataclass
class InventoryItem:
    """Representa um item empilhável armazenado dentro do Inventory (Composição)."""

    name: str
    description: str
    count: int
    itemType: str
