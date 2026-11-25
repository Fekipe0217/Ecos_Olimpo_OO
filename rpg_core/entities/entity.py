from abc import ABC, abstractmethod


class Entity(ABC):
    """Classe base abstrata para todas as entidades vivas do RPG (heróis e inimigos)."""

    def __init__(
        self,
        name: str,
        level: int,
        max_hp: int,
        max_energy: int,
        attack: int,
        defense: int,
        speed: int,
    ) -> None:
        self._name: str = name
        self._level: int = level
        self._max_hp: int = max_hp
        self._current_hp: int = max_hp
        self._max_energy: int = max_energy
        self._current_energy: int = max_energy
        self._attack: int = attack
        self._defense: int = defense
        self._speed: int = speed
        self._is_defending: bool = False
        self._status_effects: dict[str, int] = {}

    def getName(self) -> str:
        return self._name

    def getLevel(self) -> int:
        return self._level

    def getCurrentHp(self) -> int:
        return self._current_hp

    def getMaxHp(self) -> int:
        return self._max_hp

    def getCurrentEnergy(self) -> int:
        return self._current_energy

    def getMaxEnergy(self) -> int:
        return self._max_energy

    def getAttack(self) -> int:
        return self._attack

    def getDefense(self) -> int:
        return self._defense

    def getSpeed(self) -> int:
        return self._speed

    def isDefending(self) -> bool:
        return self._is_defending

    def isAlive(self) -> bool:
        return self._current_hp > 0

    def heal(self, amount: int) -> int:
        """Restaura HP até o máximo e retorna a quantidade efetivamente curada."""
        if amount <= 0 or not self.isAlive():
            return 0
        previous_hp = self._current_hp
        self._current_hp = min(self._max_hp, self._current_hp + amount)
        return self._current_hp - previous_hp

    def restoreEnergy(self, amount: int) -> int:
        """Restaura energia até o máximo e retorna a quantidade recuperada."""
        if amount <= 0:
            return 0
        previous_energy = self._current_energy
        self._current_energy = min(self._max_energy, self._current_energy + amount)
        return self._current_energy - previous_energy

    def consumeEnergy(self, amount: int) -> bool:
        """Consome energia se houver saldo suficiente."""
        if amount < 0 or self._current_energy < amount:
            return False
        self._current_energy -= amount
        return True

    def setDefending(self, status: bool) -> None:
        self._is_defending = status

    def takeDamage(self, rawDamage: int, type: str = "physical", isCrit: bool = False) -> int:
        """Calcula e aplica o dano recebido considerando crítico, defesa e postura defensiva."""
        effective_raw = int(rawDamage * 1.5) if isCrit else rawDamage
        mitigation = self._defense if type == "physical" else int(self._defense * 0.6)
        damage = max(1, effective_raw - mitigation)

        if self._is_defending:
            damage = max(1, damage // 2)

        self._current_hp = max(0, self._current_hp - damage)
        return damage

    # POLIMORFISMO: métodos abstratos que obrigam as subclasses a definir comportamentos próprios
    @abstractmethod
    def applyTurnStartPassive(self) -> list[str]:
        """Aplica habilidades passivas no início do turno e retorna mensagens de log."""
        raise NotImplementedError

    @abstractmethod
    def getRoleDescription(self) -> str:
        """Retorna a descrição do papel da entidade no combate."""
        raise NotImplementedError
