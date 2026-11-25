import random

from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.enemies.enemy import Enemy
from rpg_core.entities.entity import Entity


# HERANÇA: CerberusOfUnderworld herda de Enemy
class CerberusOfUnderworld(Enemy):
    """Cérbero do Submundo: cão de três cabeças com bafo infernal e mordida tripla."""

    def __init__(self) -> None:
        super().__init__(
            name="Cérbero",
            title="Guardião de Três Cabeças do Submundo",
            level=4,
            max_hp=220,
            max_energy=70,
            attack=27,
            defense=10,
            speed=14,
            xp_reward=300,
        )

    # POLIMORFISMO e DEPENDÊNCIA: implementa takeTurnAi() usando player (Entity) e retornando AbilityResult
    def takeTurnAi(self, player: Entity) -> AbilityResult:
        """Executa Sopro Infernal (queimadura) ou Mordida Tripla."""
        self.restoreEnergy(8)

        if self._current_energy >= 25 and random.random() < 0.50:
            self.consumeEnergy(25)
            is_crit = random.random() < 0.20
            raw_damage = int(self._attack * 1.45)
            damage = player.takeDamage(raw_damage, type="fire", isCrit=is_crit)
            crit_text = " (CRÍTICO!)" if is_crit else ""
            return AbilityResult(
                success=True,
                damage_dealt=damage,
                is_crit=is_crit,
                message=(
                    f"{self._name} exalou Sopro Infernal{crit_text} em {player.getName()}, "
                    f"causando {damage} de dano!"
                ),
            )

        is_crit = random.random() < 0.25
        raw_damage = int(self._attack * 1.15)
        damage = player.takeDamage(raw_damage, type="physical", isCrit=is_crit)
        crit_text = " (CRÍTICO!)" if is_crit else ""
        return AbilityResult(
            success=True,
            damage_dealt=damage,
            is_crit=is_crit,
            message=f"{self._name} desferiu Mordida Tripla{crit_text}, causando {damage} de dano!",
        )

    def getRoleDescription(self) -> str:
        return f"{self._name} — {self._title} (Nv.{self._level} | {self._xp_reward} XP)"
