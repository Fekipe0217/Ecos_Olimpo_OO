import random

from rpg_core.characters.demigod import Demigod
from rpg_core.entities.entity import Entity


# HERANÇA: ChildOfZeus herda de Demigod (e indiretamente de Entity)
class ChildOfZeus(Demigod):
    """Subclasse de semideus descendente de Zeus, especializado em cargas estáticas."""

    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            divine_parent="Zeus",
            level=1,
            max_hp=110,
            max_energy=70,
            attack=20,
            defense=6,
            speed=14,
        )
        self._staticCharges: int = 0

    def getStaticCharges(self) -> int:
        return self._staticCharges

    # POLIMORFISMO: sobrescreve applyTurnStartPassive() com mecânica de cargas estáticas
    def applyTurnStartPassive(self) -> list[str]:
        """Acumula carga estática e recupera um pouco de energia no início do turno."""
        logs: list[str] = []
        if self._staticCharges < 3:
            self._staticCharges += 1
            logs.append(
                f"[Passiva - Zeus] {self._name} acumulou 1 carga estática "
                f"({self._staticCharges}/3)."
            )
        recovered = self.restoreEnergy(5)
        if recovered > 0:
            logs.append(f"[Passiva - Zeus] {self._name} recuperou +{recovered} de energia.")
        return logs

    # POLIMORFISMO e DEPENDÊNCIA: sobrescreve basicAttack() descarregando estática em target (Entity)
    def basicAttack(self, target: Entity) -> int:
        """Ataca o alvo; se tiver 3 cargas estáticas, descarrega dano elétrico bônus."""
        is_crit = random.random() < 0.15
        if self._staticCharges >= 3:
            self._staticCharges = 0
            bonus_damage = self._attack + 12
            return target.takeDamage(bonus_damage, type="lightning", isCrit=is_crit)
        return target.takeDamage(self._attack, type="physical", isCrit=is_crit)

    # POLIMORFISMO: sobrescreve getRoleDescription()
    def getRoleDescription(self) -> str:
        return (
            f"{self._name} — Filho(a) de Zeus (Nv.{self._level}) | "
            f"Cargas Estáticas: {self._staticCharges}/3"
        )
