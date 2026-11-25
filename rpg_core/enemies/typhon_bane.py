import random

from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.enemies.enemy import Enemy
from rpg_core.entities.entity import Entity


# HERANÇA: TyphonBane herda de Enemy
class TyphonBane(Enemy):
    """Tifão, Pai dos Monstros: chefe final com fúria das tempestades e ataques cataclísmicos."""

    def __init__(self) -> None:
        super().__init__(
            name="Tifão",
            title="Flagelo dos Deuses e Pai dos Monstros",
            level=5,
            max_hp=290,
            max_energy=90,
            attack=31,
            defense=12,
            speed=16,
            xp_reward=500,
        )

    # POLIMORFISMO: sobrescreve applyTurnStartPassive() com regeneração titânica e energia
    def applyTurnStartPassive(self) -> list[str]:
        """Tifão absorve o caos da tempestade para recuperar energia e HP."""
        logs: list[str] = []
        energy_gain = self.restoreEnergy(12)
        healed = self.heal(10)
        if healed > 0 or energy_gain > 0:
            logs.append(
                f"[Passiva - Tifão] A fúria primordial restaurou +{healed} HP e +{energy_gain} Energia!"
            )
        return logs

    # POLIMORFISMO e DEPENDÊNCIA: implementa takeTurnAi() usando player (Entity) e retornando AbilityResult
    def takeTurnAi(self, player: Entity) -> AbilityResult:
        """Alterna entre Tempestade Cataclísmica, Golpe Sísmico e postura defensiva."""
        if self._current_energy >= 30 and random.random() < 0.55:
            self.consumeEnergy(30)
            is_crit = random.random() < 0.25
            raw_damage = int(self._attack * 1.55)
            damage = player.takeDamage(raw_damage, type="lightning", isCrit=is_crit)
            crit_text = " (CRÍTICO!)" if is_crit else ""
            return AbilityResult(
                success=True,
                damage_dealt=damage,
                is_crit=is_crit,
                message=(
                    f"{self._name} desencadeou Tempestade Cataclísmica{crit_text} em "
                    f"{player.getName()}, causando {damage} de dano!"
                ),
            )

        if self._current_hp < self._max_hp * 0.30 and random.random() < 0.25:
            self.setDefending(True)
            return AbilityResult(
                success=True,
                message=f"{self._name} envolveu-se em ventos impenetráveis e assumiu postura defensiva!",
            )

        is_crit = random.random() < 0.20
        damage = player.takeDamage(self._attack, type="physical", isCrit=is_crit)
        crit_text = " (CRÍTICO!)" if is_crit else ""
        return AbilityResult(
            success=True,
            damage_dealt=damage,
            is_crit=is_crit,
            message=f"{self._name} esmagou o chão com Impacto Titânico{crit_text}, causando {damage} de dano!",
        )

    def getRoleDescription(self) -> str:
        return f"{self._name} — {self._title} (Nv.{self._level} | {self._xp_reward} XP)"
