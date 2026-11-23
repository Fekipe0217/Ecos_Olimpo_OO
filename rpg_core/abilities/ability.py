from rpg_core.entities.entity import Entity


class Ability:
    """Representa uma habilidade especial utilizável em combate."""

    def __init__(self, name: str, description: str, base_damage: int = 25) -> None:
        self._name: str = name
        self._description: str = description
        self._base_damage: int = base_damage

    def getName(self) -> str:
        return self._name

    # DEPENDÊNCIA: execute() depende temporariamente das instâncias user e target (Entity)
    def execute(self, user: Entity, target: Entity) -> int:
        """Executa a habilidade de user contra target e retorna o dano causado."""
        return target.takeDamage(self._base_damage, type="special", isCrit=False)
