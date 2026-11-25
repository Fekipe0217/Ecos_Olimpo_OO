import random

from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.enemies.enemy import Enemy
from rpg_core.entities.entity import Entity


# HERANÇA: LernaeanHydra herda de Enemy
class LernaeanHydra(Enemy):
    """Hidra de Lerna: regenera cabeças no início do turno e aplica veneno mortal."""

    def __init__(self) -> None:
        super().__init__(
            name="Hidra de Lerna",
            title="Serpente Imortal dos Pântanos",
            level=2,
            max_hp=155,
            max_energy=50,
            attack=20,
            defense=6,
            speed=11,
            xp_reward=160,
        )

    # POLIMORFISMO: sobrescreve applyTurnStartPassive() com regeneração de cabeças
    def applyTurnStartPassive(self) -> list[str]:
        """Regenera HP no início do turno simulando novas cabeças crescendo."""
        logs: list[str] = []
        if self.isAlive() and self._current_hp < self._max_hp:
            healed = self.heal(8)
            if healed > 0:
                logs.append(
                    f"[Passiva - Hidra] {self._name} regenerou uma cabeça e recuperou +{healed} HP!"
                )
        return logs

    # POLIMORFISMO e DEPENDÊNCIA: implementa takeTurnAi() usando player (Entity) e retornando AbilityResult
    def takeTurnAi(self, player: Entity) -> AbilityResult:
        """Alterna entre mordida venenosa e investida múltipla das cabeças."""
        self.restoreEnergy(6)

        if self._current_energy >= 18 and random.random() < 0.50:
            self.consumeEnergy(18)
            is_crit = random.random() < 0.18
            raw_damage = int(self._attack * 1.35)
            damage = player.takeDamage(raw_damage, type="poison", isCrit=is_crit)
            crit_text = " (CRÍTICO!)" if is_crit else ""
            return AbilityResult(
                success=True,
                damage_dealt=damage,
                is_crit=is_crit,
                message=(
                    f"{self._name} desferiu Mordida Venenosa{crit_text} em "
                    f"{player.getName()}, causando {damage} de dano!"
                ),
            )

        damage = player.takeDamage(self._attack, type="physical", isCrit=False)
        return AbilityResult(
            success=True,
            damage_dealt=damage,
            message=f"{self._name} atacou {player.getName()} com múltiplas cabeças, causando {damage} de dano!",
        )

    def getRoleDescription(self) -> str:
        return f"{self._name} — {self._title} (Nv.{self._level} | {self._xp_reward} XP)"
