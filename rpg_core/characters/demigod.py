from abc import ABC
import random

from rpg_core.abilities.ability import Ability
from rpg_core.entities.entity import Entity
from rpg_core.items.inventory import Inventory


# HERANÇA: Demigod herda atributos e métodos base de Entity
class Demigod(Entity, ABC):
    """Classe base abstrata para todos os heróis semideuses controláveis."""

    def __init__(
        self,
        name: str,
        divine_parent: str,
        level: int = 1,
        max_hp: int = 100,
        max_energy: int = 60,
        attack: int = 18,
        defense: int = 6,
        speed: int = 12,
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
        self._divine_parent: str = divine_parent
        self._xp: int = 0
        self._xp_to_next: int = 100

        # ASSOCIAÇÃO: Demigod mantém referências a instâncias de Ability criadas externamente
        self._abilities: list[Ability] = []

        # COMPOSIÇÃO: Demigod cria e é dono exclusivo do ciclo de vida do seu Inventory
        self._inventory: Inventory = Inventory()

    def getDivineParent(self) -> str:
        return self._divine_parent

    def getXp(self) -> int:
        return self._xp

    def getXpToNext(self) -> int:
        return self._xp_to_next

    def addAbility(self, ability: Ability) -> None:
        """Associa uma habilidade ao semideus."""
        self._abilities.append(ability)

    def getAbilities(self) -> list[Ability]:
        return list(self._abilities)

    def clearAbilities(self) -> None:
        self._abilities.clear()

    def getInventory(self) -> Inventory:
        return self._inventory

    def restoreState(
        self,
        level: int,
        xp: int,
        xp_to_next: int,
        max_hp: int,
        current_hp: int,
        max_energy: int,
        current_energy: int,
        attack: int,
        defense: int,
        speed: int,
    ) -> None:
        """Restaura os atributos do semideus a partir de um save do banco de dados."""
        self._level = level
        self._xp = xp
        self._xp_to_next = xp_to_next
        self._max_hp = max_hp
        self._current_hp = max(1, min(max_hp, current_hp))
        self._max_energy = max_energy
        self._current_energy = max(0, min(max_energy, current_energy))
        self._attack = attack
        self._defense = defense
        self._speed = speed

    def gainXp(self, amount: int) -> None:
        """Adiciona XP e realiza level up automaticamente ao atingir o limite."""
        if amount <= 0:
            return
        self._xp += amount
        while self._xp >= self._xp_to_next:
            self._xp -= self._xp_to_next
            self.levelUp()

    def levelUp(self) -> None:
        """Aumenta o nível e os atributos base do semideus, restaurando HP e Energia."""
        self._level += 1
        self._xp_to_next = int(self._xp_to_next * 1.5)
        self._max_hp += 20
        self._max_energy += 10
        self._attack += 4
        self._defense += 2
        self._speed += 2
        self._current_hp = self._max_hp
        self._current_energy = self._max_energy

    # DEPENDÊNCIA: recebe uma Entity como alvo do ataque básico
    def basicAttack(self, target: Entity) -> int:
        """Executa um ataque físico básico contra o alvo."""
        is_crit = random.random() < 0.15
        return target.takeDamage(self._attack, type="physical", isCrit=is_crit)

    def getRoleDescription(self) -> str:
        return f"Semideus {self._name} (Nv.{self._level}), filho(a) de {self._divine_parent}."
