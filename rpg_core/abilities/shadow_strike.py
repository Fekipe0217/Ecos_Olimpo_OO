import random

from rpg_core.abilities.ability import Ability
from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.entities.entity import Entity


# HERANÇA: ShadowStrike herda de Ability
class ShadowStrike(Ability):
    """Habilidade sombria assinatura dos filhos de Hades."""

    def __init__(self) -> None:
        super().__init__(
            name="Golpe das Sombras",
            description="Ataca pelas sombras com alta chance crítica e drena vida do alvo.",
            energy_cost=22,
            cooldown=2,
            required_level=1,
            element="shadow",
        )

    # POLIMORFISMO e DEPENDÊNCIA: sobrescreve execute() recebendo Entity e retornando AbilityResult
    def execute(self, user: Entity, target: Entity) -> AbilityResult:
        if user.getLevel() < self._required_level:
            return AbilityResult(
                success=False,
                message=f"{user.getName()} precisa do nível {self._required_level} para usar {self._name}.",
            )

        if not self.isReady(user.getCurrentEnergy()):
            if self._current_cooldown > 0:
                return AbilityResult(
                    success=False,
                    message=f"{self._name} ainda está em recarga ({self._current_cooldown} turno(s)).",
                )
            return AbilityResult(
                success=False,
                message=f"Energia insuficiente para {self._name} (custo: {self._energy_cost}).",
            )

        user.consumeEnergy(self._energy_cost)
        self.triggerCooldown()

        is_crit = random.random() < 0.35
        raw_damage = int(user.getAttack() * 1.75)
        damage_dealt = target.takeDamage(raw_damage, type=self._element, isCrit=is_crit)
        healing_done = user.heal(max(4, damage_dealt // 3))

        crit_text = " (CRÍTICO!)" if is_crit else ""
        return AbilityResult(
            success=True,
            damage_dealt=damage_dealt,
            healing_done=healing_done,
            is_crit=is_crit,
            message=(
                f"{user.getName()} desferiu {self._name}{crit_text} em {target.getName()}, "
                f"causando {damage_dealt} de dano e drenando +{healing_done} HP!"
            ),
        )
