from rpg_core.characters.demigod import Demigod


# HERANÇA: ChildOfPoseidon herda de Demigod (e de Entity)
class ChildOfPoseidon(Demigod):
    """Subclasse de semideus descendente de Poseidon, com regeneração e resistência marinha."""

    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            divine_parent="Poseidon",
            level=1,
            max_hp=125,
            max_energy=65,
            attack=18,
            defense=8,
            speed=12,
        )

    # POLIMORFISMO: sobrescreve applyTurnStartPassive() com bênção regenerativa dos mares
    def applyTurnStartPassive(self) -> list[str]:
        """Regenera parte do HP e da Energia no início de cada turno."""
        logs: list[str] = []
        healed = self.heal(6)
        if healed > 0:
            logs.append(f"[Passiva - Poseidon] {self._name} regenerou +{healed} HP com a maré.")
        energy_gain = self.restoreEnergy(6)
        if energy_gain > 0:
            logs.append(f"[Passiva - Poseidon] {self._name} recuperou +{energy_gain} de energia.")
        return logs

    # POLIMORFISMO: sobrescreve takeDamage() oferecendo resistência elemental/física dos oceanos
    def takeDamage(self, rawDamage: int, type: str = "physical", isCrit: bool = False) -> int:
        """Reduz o dano recebido graças à proteção aquática (especialmente contra fogo e água)."""
        base_taken = super().takeDamage(rawDamage, type=type, isCrit=isCrit)
        if type in ("fire", "water"):
            reduced = max(1, int(base_taken * 0.70))
        else:
            reduced = max(1, int(base_taken * 0.85))
        diff = base_taken - reduced
        if diff > 0 and self._current_hp > 0:
            self._current_hp = min(self._max_hp, self._current_hp + diff)
        return reduced

    # POLIMORFISMO: sobrescreve getRoleDescription()
    def getRoleDescription(self) -> str:
        return (
            f"{self._name} — Filho(a) de Poseidon (Nv.{self._level}) | "
            f"Resistência Marinha & Regeneração"
        )
