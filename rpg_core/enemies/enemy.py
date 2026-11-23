from rpg_core.entities.entity import Entity


# HERANÇA: Enemy herda de Entity
class Enemy(Entity):
    """Classe base para os monstros e inimigos do jogo."""

    def __init__(
        self,
        name: str,
        title: str,
        max_hp: int = 80,
        attack: int = 14,
        defense: int = 3,
        xp_reward: int = 50,
    ) -> None:
        super().__init__(name=name, max_hp=max_hp, attack=attack, defense=defense)
        self._title: str = title
        self._xp_reward: int = xp_reward

    # DEPENDÊNCIA: o turno do inimigo depende da entidade jogador passada por parâmetro
    def takeTurnAi(self, player: Entity) -> int:
        """Executa a ação simples de ataque do inimigo contra o jogador."""
        return player.takeDamage(self._attack, type="physical", isCrit=False)

    # POLIMORFISMO: implementação específica de getRoleDescription() para Enemy
    def getRoleDescription(self) -> str:
        return f"Inimigo {self._name}, {self._title} (Recompensa: {self._xp_reward} XP)."
