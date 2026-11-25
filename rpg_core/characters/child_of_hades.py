import random

from rpg_core.characters.demigod import Demigod
from rpg_core.entities.entity import Entity


# HERANÇA: ChildOfHades herda de Demigod (e de Entity)
class ChildOfHades(Demigod):
    """Subclasse de semideus descendente de Hades, especializado em drenagem vital e sombras."""

    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            divine_parent="Hades",
            level=1,
            max_hp=105,
            max_energy=75,
            attack=21,
            defense=6,
            speed=15,
        )

    # POLIMORFISMO: sobrescreve applyTurnStartPassive() com aura sombria
    def applyTurnStartPassive(self) -> list[str]:
        """Recupera energia sombria no início do turno."""
        logs: list[str] = []
        energy_gain = self.restoreEnergy(7)
        if energy_gain > 0:
            logs.append(
                f"[Passiva - Hades] {self._name} absorveu energia das sombras (+{energy_gain} Energia)."
            )
        return logs

    # POLIMORFISMO e DEPENDÊNCIA: sobrescreve basicAttack() aplicando roubo de vida ao atingir target (Entity)
    def basicAttack(self, target: Entity) -> int:
        """Executa golpe sombrio com maior chance crítica e drena parte do dano como HP."""
        is_crit = random.random() < 0.25
        damage = target.takeDamage(self._attack, type="shadow", isCrit=is_crit)
        self.heal(max(1, damage // 3))
        return damage

    # POLIMORFISMO: sobrescreve getRoleDescription()
    def getRoleDescription(self) -> str:
        return (
            f"{self._name} — Filho(a) de Hades (Nv.{self._level}) | "
            f"Drenagem Vital & Golpe Sombrio"
        )
