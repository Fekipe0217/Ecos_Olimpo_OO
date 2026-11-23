from rpg_core.abilities.ability import Ability
from rpg_core.entities.entity import Entity
from rpg_core.items.inventory import Inventory


# HERANÇA: Demigod herda atributos e comportamentos básicos de Entity
class Demigod(Entity):
    """Representa o herói semideus controlado pelo jogador."""

    def __init__(
        self,
        name: str,
        divine_parent: str,
        max_hp: int = 100,
        attack: int = 18,
        defense: int = 5,
    ) -> None:
        super().__init__(name=name, max_hp=max_hp, attack=attack, defense=defense)
        self._divine_parent: str = divine_parent

        # ASSOCIAÇÃO: Demigod mantém referências a objetos Ability criados externamente
        self._abilities: list[Ability] = []

        # COMPOSIÇÃO: Demigod instancia e é dono exclusivo do ciclo de vida do seu Inventory
        self._inventory: Inventory = Inventory()

    def addAbility(self, ability: Ability) -> None:
        """Associa uma habilidade ao semideus."""
        self._abilities.append(ability)

    def getAbilities(self) -> list[Ability]:
        return self._abilities

    def getInventory(self) -> Inventory:
        return self._inventory

    # DEPENDÊNCIA: utiliza outra Entity temporariamente como alvo do ataque
    def basicAttack(self, target: Entity) -> int:
        """Executa um ataque básico contra uma entidade alvo."""
        return target.takeDamage(self._attack, type="physical", isCrit=False)

    # POLIMORFISMO: implementação específica de getRoleDescription() para Demigod
    def getRoleDescription(self) -> str:
        return f"Semideus {self._name}, filho(a) de {self._divine_parent}."
