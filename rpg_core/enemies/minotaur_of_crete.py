import random

from rpg_core.abilities.ability_result import AbilityResult
from rpg_core.enemies.enemy import Enemy
from rpg_core.entities.entity import Entity


# HERANÇA: MinotaurOfCrete herda de Enemy
class MinotaurOfCrete(Enemy):
    """Monstro Minotauro de Creta com ataques brutais e investida de chifres."""

    def __init__(self) -> None:
        super().__init__(
            name="Minotauro",
            title="Besta do Labirinto de Creta",
            level=1,
            max_hp=120,
            max_energy=40,
            attack=17,
            defense=5,
            speed=10,
            xp_reward=100,
        )

    # POLIMORFISMO e DEPENDÊNCIA: implementa takeTurnAi() usando player (Entity) e retornando AbilityResult
    def takeTurnAi(self, player: Entity) -> AbilityResult:
        """Executa Investida de Chifres se tiver energia ou golpe físico padrão."""
        self.restoreEnergy(5)

        if self._current_energy >= 20 and random.random() < 0.45:
            self.consumeEnergy(20)
            is_crit = random.random() < 0.20
            raw_damage = int(self._attack * 1.45)
            damage = player.takeDamage(raw_damage, type="physical", isCrit=is_crit)
            status = ""
            if player.isAlive() and random.random() < 0.35:
                player.addStatusEffect("bleed", 2)
                status = "bleed"
            crit_text = " (CRÍTICO!)" if is_crit else ""
            status_text = " e causou sangramento!" if status else "!"
            return AbilityResult(
                success=True,
                damage_dealt=damage,
                is_crit=is_crit,
                status_applied=status,
                message=(
                    f"{self._name} executou Investida de Chifres{crit_text} em "
                    f"{player.getName()}, causando {damage} de dano{status_text}"
                ),
            )

        if self._current_hp < self._max_hp * 0.35 and random.random() < 0.30:
            self.setDefending(True)
            return AbilityResult(
                success=True,
                message=f"{self._name} ergueu a guarda e entrou em postura defensiva!",
            )

        damage = player.takeDamage(self._attack, type="physical", isCrit=False)
        return AbilityResult(
            success=True,
            damage_dealt=damage,
            message=f"{self._name} golpeou {player.getName()} com seu machado, causando {damage} de dano!",
        )

    # POLIMORFISMO: sobrescreve getRoleDescription()
    def getRoleDescription(self) -> str:
        return f"{self._name} — {self._title} (Nv.{self._level} | {self._xp_reward} XP)"
