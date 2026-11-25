from abc import ABC, abstractmethod

from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.entities.entity import Entity


class Ability(ABC):
    """Classe base abstrata para habilidades especiais de combate."""

    def __init__(
        self,
        name: str,
        description: str,
        energy_cost: int,
        cooldown: int,
        required_level: int,
        element: str,
    ) -> None:
        self._name: str = name
        self._description: str = description
        self._energy_cost: int = energy_cost
        self._cooldown: int = cooldown
        self._current_cooldown: int = 0
        self._required_level: int = required_level
        self._element: str = element

    def getName(self) -> str:
        return self._name

    def getDescription(self) -> str:
        return self._description

    def getEnergyCost(self) -> int:
        return self._energy_cost

    def getCooldown(self) -> int:
        return self._cooldown

    def getCurrentCooldown(self) -> int:
        return self._current_cooldown

    def setCurrentCooldown(self, cooldown: int) -> None:
        self._current_cooldown = max(0, min(self._cooldown, cooldown))

    def getRequiredLevel(self) -> int:
        return self._required_level

    def getElement(self) -> str:
        return self._element

    def isReady(self, energy: int) -> bool:
        """Verifica se a habilidade está fora de recarga e se há energia suficiente."""
        return self._current_cooldown == 0 and energy >= self._energy_cost

    def triggerCooldown(self) -> None:
        """Ativa o tempo de recarga da habilidade após o uso."""
        self._current_cooldown = self._cooldown

    def tickCooldown(self) -> None:
        """Reduz o tempo de recarga em 1 turno, se houver."""
        if self._current_cooldown > 0:
            self._current_cooldown -= 1

    # POLIMORFISMO e DEPENDÊNCIA: cada subclasse implementa execute recebendo Entity e retornando AbilityResult
    @abstractmethod
    def execute(self, user: Entity, target: Entity) -> AbilityResult:
        """Executa a habilidade de user contra target."""
        raise NotImplementedError
