from abc import ABC, abstractmethod


class Entity(ABC):
    """Classe base abstrata para todas as entidades vivas do RPG (heróis e inimigos)."""

    def __init__(self, name: str, max_hp: int, attack: int, defense: int) -> None:
        self._name: str = name
        self._max_hp: int = max_hp
        self._current_hp: int = max_hp
        self._attack: int = attack
        self._defense: int = defense

    def getName(self) -> str:
        return self._name

    def getCurrentHp(self) -> int:
        return self._current_hp

    def getMaxHp(self) -> int:
        return self._max_hp

    def isAlive(self) -> bool:
        return self._current_hp > 0

    def takeDamage(self, rawDamage: int, type: str = "physical", isCrit: bool = False) -> int:
        """Aplica dano reduzido pela defesa e retorna o dano efetivo causado."""
        damage = max(1, rawDamage - self._defense)
        self._current_hp = max(0, self._current_hp - damage)
        return damage

    # POLIMORFISMO: método abstrato que obriga cada subclasse a fornecer sua própria descrição
    @abstractmethod
    def getRoleDescription(self) -> str:
        """Retorna a descrição do papel da entidade no combate."""
        raise NotImplementedError
