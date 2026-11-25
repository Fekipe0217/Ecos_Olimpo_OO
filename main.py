from rpg_core.abilities.thunderbolt import Thunderbolt
from rpg_core.characters.child_of_zeus import ChildOfZeus
from rpg_core.characters.demigod import Demigod
from rpg_core.enemies.enemy import Enemy
from rpg_core.enemies.minotaur_of_crete import MinotaurOfCrete
from rpg_core.entities.entity import Entity


def print_combat_hud(entities: list[Entity]) -> None:
    """Demonstra POLIMORFISMO exibindo o status de qualquer Entity (herói ou inimigo)."""
    print("\n" + "=" * 55)
    for entity in entities:
        defending_tag = " [DEFENDENDO]" if entity.isDefending() else ""
        print(entity.getRoleDescription() + defending_tag)
        print(
            f"  HP: {entity.getCurrentHp()}/{entity.getMaxHp()} | "
            f"Energia: {entity.getCurrentEnergy()}/{entity.getMaxEnergy()} | "
            f"ATQ: {entity.getAttack()} | DEF: {entity.getDefense()} | VEL: {entity.getSpeed()}"
        )
    print("=" * 55)


def handle_player_turn(hero: Demigod, enemy: Enemy) -> bool:
    """Executa o menu interativo do turno do jogador. Retorna True se agiu, False se fugiu/encerrou."""
    while True:
        print("\nEscolha sua ação:")
        print("  1. Ataque Básico")
        print("  2. Usar Habilidade")
        print("  3. Defender (reduz dano recebido pela metade neste turno)")
        print("  4. Usar Item do Inventário")
        print("  0. Sair do combate")

        choice = input("Opção: ").strip()

        if choice == "1":
            dmg = hero.basicAttack(enemy)
            print(f"\n[Ataque] {hero.getName()} atacou {enemy.getName()} e causou {dmg} de dano!")
            return True

        if choice == "2":
            abilities = hero.getAbilities()
            if not abilities:
                print("\n[Aviso] Nenhuma habilidade associada.")
                continue

            print("\nHabilidades disponíveis:")
            for idx, ability in enumerate(abilities, start=1):
                cd_info = (
                    f"Recarga: {ability.getCurrentCooldown()}t"
                    if ability.getCurrentCooldown() > 0
                    else "Pronta"
                )
                print(
                    f"  {idx}. {ability.getName()} (Custo: {ability.getEnergyCost()} | {cd_info})"
                )
                print(f"     {ability.getDescription()}")

            sel = input("Escolha a habilidade (ou Enter para voltar): ").strip()
            if not sel:
                continue
            if not sel.isdigit() or not (1 <= int(sel) <= len(abilities)):
                print("Seleção inválida.")
                continue

            selected_ability = abilities[int(sel) - 1]
            # DEPENDÊNCIA: execute() retorna AbilityResult
            result = selected_ability.execute(hero, enemy)
            print(f"\n[Habilidade] {result.message}")
            if result.success:
                return True

        elif choice == "3":
            hero.setDefending(True)
            print(f"\n[Defesa] {hero.getName()} assumiu postura defensiva!")
            return True

        elif choice == "4":
            items = hero.getInventory().getItems()
            if not items:
                print("\n[Inventário] Seu inventário está vazio.")
                continue

            print("\nItens no inventário:")
            for idx, item in enumerate(items, start=1):
                print(f"  {idx}. {item.name} (x{item.count}) [{item.itemType}] — {item.description}")

            sel = input("Escolha o item (ou Enter para voltar): ").strip()
            if not sel:
                continue
            if not sel.isdigit() or not (1 <= int(sel) <= len(items)):
                print("Seleção inválida.")
                continue

            chosen_item = items[int(sel) - 1]
            if hero.getInventory().useItem(chosen_item.name, hero):
                print(f"\n[Item] {hero.getName()} usou {chosen_item.name}!")
                return True
            print("Não foi possível usar este item.")

        elif choice == "0":
            return False

        else:
            print("Opção inválida. Digite 1, 2, 3, 4 ou 0.")


def run_combat(hero: Demigod, enemy: Enemy) -> None:
    """Executa o loop completo de combate em turnos no terminal."""
    turn = 1
    while hero.isAlive() and enemy.isAlive():
        print(f"\n>>> TURNO {turn} <<<")

        # Início de turno do herói
        hero.setDefending(False)
        for ability in hero.getAbilities():
            ability.tickCooldown()

        for msg in hero.applyTurnStartPassive():
            print(f"  {msg}")
        for msg in hero.processStatusEffects():
            print(f"  {msg}")

        if not hero.isAlive():
            break

        print_combat_hud([hero, enemy])
        acted = handle_player_turn(hero, enemy)
        if not acted:
            print("\nCombate encerrado pelo jogador.")
            return

        if not enemy.isAlive():
            break

        # Início de turno e ação do inimigo
        enemy.setDefending(False)
        for msg in enemy.applyTurnStartPassive():
            print(f"  {msg}")
        for msg in enemy.processStatusEffects():
            print(f"  {msg}")

        if enemy.isAlive():
            ai_result = enemy.takeTurnAi(hero)
            print(f"[Inimigo] {ai_result.message}")

        turn += 1

    print_combat_hud([hero, enemy])
    if hero.isAlive() and not enemy.isAlive():
        print(f"\nVITÓRIA! {hero.getName()} derrotou {enemy.getName()}!")
        prev_level = hero.getLevel()
        hero.gainXp(enemy.getXpReward())
        print(f"XP ganho: +{enemy.getXpReward()} (XP atual: {hero.getXp()}/{hero.getXpToNext()})")
        if hero.getLevel() > prev_level:
            print(
                f"LEVEL UP! {hero.getName()} subiu para o nível {hero.getLevel()}! "
                f"(HP Máx: {hero.getMaxHp()}, Energia Máx: {hero.getMaxEnergy()})"
            )
    elif not hero.isAlive():
        print(f"\nDERROTA! {hero.getName()} caiu em combate diante de {enemy.getName()}...")


def main() -> None:
    print("=== RPG Core - Etapa 0.2 (Combate Completo no Terminal) ===")
    hero_name = input("Digite o nome do seu Semideus (Enter para 'Thalia'): ").strip() or "Thalia"

    # 1 subclasse de herói: ChildOfZeus
    hero = ChildOfZeus(name=hero_name)

    # ASSOCIAÇÃO: habilidade criada externamente e associada ao herói
    thunderbolt = Thunderbolt()
    hero.addAbility(thunderbolt)

    # COMPOSIÇÃO: inventário interno do herói recebe itens (Inventory cria InventoryItem)
    hero.getInventory().addItem("Néctar", 2)
    hero.getInventory().addItem("Ambrosia", 1)
    hero.getInventory().addItem("Elixir Olímpico", 1)

    # 1 tipo de monstro: MinotaurOfCrete
    enemy = MinotaurOfCrete()

    print(f"\nUm inimigo surge no caminho: {enemy.getRoleDescription()}")
    run_combat(hero, enemy)


if __name__ == "__main__":
    main()
