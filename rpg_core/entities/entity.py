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

    def addStatusEffect(self, effect_name: str, duration: int) -> None:
        """Aplica ou renova um efeito de status por N turnos."""
        if effect_name and duration > 0:
            self._status_effects[effect_name] = max(
                self._status_effects.get(effect_name, 0), duration
            )

    def hasStatusEffect(self, effect_name: str) -> bool:
        return self._status_effects.get(effect_name, 0) > 0

    def processStatusEffects(self) -> list[str]:
        """Processa os efeitos de status ativos no início do turno e reduz suas durações."""
        logs: list[str] = []
        expired: list[str] = []

        for effect, turns in self._status_effects.items():
            if effect == "shock":
                shock_dmg = max(2, int(self._max_hp * 0.04))
                self._current_hp = max(0, self._current_hp - shock_dmg)
                logs.append(f"{self._name} sofreu {shock_dmg} de dano por choque elétrico!")
            elif effect == "bleed":
                bleed_dmg = max(3, int(self._max_hp * 0.05))
                self._current_hp = max(0, self._current_hp - bleed_dmg)
                logs.append(f"{self._name} sofreu {bleed_dmg} de dano por sangramento!")

            remaining = turns - 1
            if remaining <= 0:
                expired.append(effect)
            else:
                self._status_effects[effect] = remaining

        for effect in expired:
            del self._status_effects[effect]
            logs.append(f"O efeito '{effect}' em {self._name} terminou.")

        return logs

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
