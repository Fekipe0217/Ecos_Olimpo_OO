import random

from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.enemies.enemy import Enemy
from rpg_core.entities.entity import Entity


# HERANÇA: MedusaOfSarpedon herda de Enemy
class MedusaOfSarpedon(Enemy):
    """Medusa de Sarpedão: pode petrificar (atordoar) o oponente com seu olhar."""

    def __init__(self) -> None:
        super().__init__(
            name="Medusa",
            title="Górgona de Sarpedão",
            level=3,
            max_hp=180,
            max_energy=60,
            attack=23,
            defense=8,
            speed=15,
            xp_reward=220,
        )

    # POLIMORFISMO e DEPENDÊNCIA: implementa takeTurnAi() usando player (Entity) e retornando AbilityResult
    def takeTurnAi(self, player: Entity) -> AbilityResult:
        """Usa Olhar Petrificante ou ataque com serpentes e garras."""
        self.restoreEnergy(8)

        if self._current_energy >= 24 and random.random() < 0.45:
            self.consumeEnergy(24)
            raw_damage = int(self._attack * 1.35)
            damage = player.takeDamage(raw_damage, type="shadow", isCrit=False)
            return AbilityResult(
                success=True,
                damage_dealt=damage,
                message=(
                    f"{self._name} lançou Olhar Petrificante em {player.getName()}, "
                    f"causando {damage} de dano!"
                ),
            )

        is_crit = random.random() < 0.22
        damage = player.takeDamage(self._attack, type="physical", isCrit=is_crit)
        crit_text = " (CRÍTICO!)" if is_crit else ""
        return AbilityResult(
            success=True,
            damage_dealt=damage,
            is_crit=is_crit,
            message=f"{self._name} atacou com garras e serpentes{crit_text}, causando {damage} de dano!",
        )

    def getRoleDescription(self) -> str:
        return f"{self._name} — {self._title} (Nv.{self._level} | {self._xp_reward} XP)"
