from rpg_core.abilities.ability import Ability
from rpg_core.characters.demigod import Demigod
from rpg_core.enemies.enemy import Enemy
from rpg_core.entities.entity import Entity


def print_status(entities: list[Entity]) -> None:
    """Demonstra POLIMORFISMO tratando Demigod e Enemy pela interface comum Entity."""
    print("\n--- Estado das Entidades ---")
    for entity in entities:
        print(f"  {entity.getRoleDescription()} | HP: {entity.getCurrentHp()}/{entity.getMaxHp()}")


def main() -> None:
    print("=== RPG Core - Etapa 0.1 (MVP de Terminal) ===")

    # Instancia herói (Demigod) e inimigo (Enemy)
    hero = Demigod(name="Percy", divine_parent="Poseidon", max_hp=100, attack=18, defense=5)
    monster = Enemy(name="Minotauro", title="Guardião do Labirinto", max_hp=70, attack=14, defense=3)

    # Associação: habilidade criada externamente e associada ao herói
    wave_strike = Ability(name="Golpe das Marés", description="Ataque de água concentrado", base_damage=28)
    hero.addAbility(wave_strike)

    # Composição: inventário já nasce dentro do herói
    hero.getInventory().addItem("Néctar", 2)

    print_status([hero, monster])

    # Turno 1: Ataque básico do herói
    dmg_basic = hero.basicAttack(monster)
    print(f"\n[Ação] {hero.getName()} usou ataque básico em {monster.getName()} e causou {dmg_basic} de dano!")

    # Turno 2: Inimigo ataca
    dmg_enemy = monster.takeTurnAi(hero)
    print(f"[Ação] {monster.getName()} atacou {hero.getName()} e causou {dmg_enemy} de dano!")

    # Turno 3: Herói usa item do inventário
    used = hero.getInventory().useItem("Néctar", hero)
    print(f"[Item] {hero.getName()} usou Néctar? {'Sim' if used else 'Não'} | Itens restantes: {hero.getInventory().getItems()}")

    # Turno 4: Herói usa habilidade associada
    dmg_skill = hero.getAbilities()[0].execute(hero, monster)
    print(f"[Habilidade] {hero.getName()} usou '{wave_strike.getName()}' em {monster.getName()} e causou {dmg_skill} de dano!")

    print_status([hero, monster])
    print("\n=== Fim do teste da Etapa 0.1 ===")


if __name__ == "__main__":
    main()
