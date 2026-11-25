from abc import ABC, abstractmethod

from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.entities.entity import Entity


# HERANÇA: Enemy herda de Entity
class Enemy(Entity, ABC):
    """Classe base abstrata para todos os monstros e chefes do RPG."""

    def __init__(
        self,
        name: str,
        title: str,
        level: int,
        max_hp: int,
        max_energy: int,
        attack: int,
        defense: int,
        speed: int,
        xp_reward: int,
    ) -> None:
        super().__init__(
            name=name,
            level=level,
            max_hp=max_hp,
            max_energy=max_energy,
            attack=attack,
            defense=defense,
            speed=speed,
        )
        self._xp_reward: int = xp_reward
        self._title: str = title

    def getXpReward(self) -> int:
        return self._xp_reward

    def getTitle(self) -> str:
        return self._title

    def applyTurnStartPassive(self) -> list[str]:
        """Passiva padrão vazia para inimigos que não possuem regeneração especial."""
        return []

    # POLIMORFISMO e DEPENDÊNCIA: cada subclasse de Enemy define sua IA usando Entity e retornando AbilityResult
    @abstractmethod
    def takeTurnAi(self, player: Entity) -> AbilityResult:
        """Decide e executa a ação do inimigo contra o jogador."""
        raise NotImplementedError

    def getRoleDescription(self) -> str:
        return f"{self._name}, {self._title} (Nv.{self._level} | Recompensa: {self._xp_reward} XP)"
