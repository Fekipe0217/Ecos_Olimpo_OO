from dataclasses import dataclass


@dataclass
class AbilityResult:
    """Objeto de transferência retornado por habilidades e turnos de inimigos (Dependência)."""

    success: bool
    damage_dealt: int = 0
    healing_done: int = 0
    is_crit: bool = False
    status_applied: str = ""
    message: str = ""
