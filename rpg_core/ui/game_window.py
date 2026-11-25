import tkinter as tk
from tkinter import messagebox, scrolledtext

from rpg_core.abilities.shadow_strike import ShadowStrike
from rpg_core.abilities.thunderbolt import Thunderbolt
from rpg_core.abilities.tidal_surge import TidalSurge
from rpg_core.characters.child_of_hades import ChildOfHades
from rpg_core.characters.child_of_poseidon import ChildOfPoseidon
from rpg_core.characters.child_of_zeus import ChildOfZeus
from rpg_core.characters.demigod import Demigod
from rpg_core.enemies.cerberus_of_underworld import CerberusOfUnderworld
from rpg_core.enemies.enemy import Enemy
from rpg_core.enemies.lernaean_hydra import LernaeanHydra
from rpg_core.enemies.medusa_of_sarpedon import MedusaOfSarpedon
from rpg_core.enemies.minotaur_of_crete import MinotaurOfCrete
from rpg_core.enemies.typhon_bane import TyphonBane
from rpg_core.persistence.save_manager import SaveManager


CAMPAIGN_BOSSES: list[type[Enemy]] = [
    MinotaurOfCrete,
    LernaeanHydra,
    MedusaOfSarpedon,
    CerberusOfUnderworld,
    TyphonBane,
]


class RpgDesktopApp(tk.Tk):
    """Interface gráfica desktop crua e funcional em tkinter para o RPG Core."""

    def __init__(self) -> None:
        super().__init__()
        self.title("RPG Core — Mitologia Grega (Desktop)")
        self.geometry("920x680")
        self.minsize(820, 600)

        self.save_manager = SaveManager("rpg_saves.db")
        self.slot_name: str = "aventura_1"
        self.stage_index: int = 0
        self.enemies_defeated: int = 0
        self.turn: int = 1
        self.in_combat: bool = True

        self.hero: Demigod = self._build_default_hero("Thalia", "ChildOfZeus")
        self.enemy: Enemy = self._create_enemy_for_stage(self.stage_index)

        self._ability_buttons: list[tk.Button] = []
        self._build_widgets()

        self._log("=== Bem-vindo ao RPG Core (Etapa 0.4 — Tkinter) ===")
        self._log("Dica: Você já pode lutar agora ou clicar em 'Novo Jogo' / 'Carregar' no topo.")
        self._start_encounter(log_header=True)

    def _build_default_hero(self, name: str, hero_class: str) -> Demigod:
        if hero_class == "ChildOfPoseidon":
            hero: Demigod = ChildOfPoseidon(name)
            hero.addAbility(TidalSurge())
        elif hero_class == "ChildOfHades":
            hero = ChildOfHades(name)
            hero.addAbility(ShadowStrike())
        else:
            hero = ChildOfZeus(name)
            hero.addAbility(Thunderbolt())

        hero.getInventory().addItem("Néctar", 3)
        hero.getInventory().addItem("Ambrosia", 1)
        hero.getInventory().addItem("Elixir Olímpico", 1)
        return hero

    def _create_enemy_for_stage(self, stage_index: int) -> Enemy:
        if stage_index < len(CAMPAIGN_BOSSES):
            return CAMPAIGN_BOSSES[stage_index]()
        return TyphonBane()

    def _build_widgets(self) -> None:
        # 1. Barra superior: Novo Jogo, Salvar, Carregar e Info da campanha
        top_frame = tk.Frame(self, padx=10, pady=8, bd=1, relief=tk.GROOVE)
        top_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        tk.Button(top_frame, text="Novo Jogo", width=12, command=self._open_new_game_dialog).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(top_frame, text="Salvar", width=10, command=self._save_current_game).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(top_frame, text="Carregar", width=10, command=self._open_load_dialog).pack(
            side=tk.LEFT, padx=3
        )

        self.campaign_info_var = tk.StringVar()
        tk.Label(
            top_frame,
            textvariable=self.campaign_info_var,
            font=("TkDefaultFont", 10, "bold"),
        ).pack(side=tk.RIGHT, padx=6)

        # 2. Área de status: Herói vs Inimigo
        status_frame = tk.Frame(self, padx=10, pady=4)
        status_frame.pack(fill=tk.X)
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=1)

        # Painel do Herói
        hero_box = tk.LabelFrame(status_frame, text="Herói (Jogador)", padx=10, pady=8)
        hero_box.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.hero_desc_var = tk.StringVar()
        tk.Label(hero_box, textvariable=self.hero_desc_var, anchor="w", font=("TkDefaultFont", 10, "bold")).pack(
            fill=tk.X
        )

        self.hero_hp_var = tk.StringVar()
        tk.Label(hero_box, textvariable=self.hero_hp_var, anchor="w").pack(fill=tk.X, pady=(6, 0))
        self.hero_hp_canvas = tk.Canvas(hero_box, height=18, bg="#dddddd", highlightthickness=1, highlightbackground="#888888")
        self.hero_hp_canvas.pack(fill=tk.X, pady=(2, 4))

        self.hero_en_var = tk.StringVar()
        tk.Label(hero_box, textvariable=self.hero_en_var, anchor="w").pack(fill=tk.X)
        self.hero_en_canvas = tk.Canvas(hero_box, height=16, bg="#dddddd", highlightthickness=1, highlightbackground="#888888")
        self.hero_en_canvas.pack(fill=tk.X, pady=(2, 4))

        self.hero_stats_var = tk.StringVar()
        tk.Label(hero_box, textvariable=self.hero_stats_var, anchor="w", fg="#333333").pack(fill=tk.X)

        # Painel do Inimigo
        enemy_box = tk.LabelFrame(status_frame, text="Inimigo", padx=10, pady=8)
        enemy_box.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        self.enemy_desc_var = tk.StringVar()
        tk.Label(enemy_box, textvariable=self.enemy_desc_var, anchor="w", font=("TkDefaultFont", 10, "bold")).pack(
            fill=tk.X
        )

        self.enemy_hp_var = tk.StringVar()
        tk.Label(enemy_box, textvariable=self.enemy_hp_var, anchor="w").pack(fill=tk.X, pady=(6, 0))
        self.enemy_hp_canvas = tk.Canvas(enemy_box, height=18, bg="#dddddd", highlightthickness=1, highlightbackground="#888888")
        self.enemy_hp_canvas.pack(fill=tk.X, pady=(2, 4))

        self.enemy_en_var = tk.StringVar()
        tk.Label(enemy_box, textvariable=self.enemy_en_var, anchor="w").pack(fill=tk.X)
        self.enemy_en_canvas = tk.Canvas(enemy_box, height=16, bg="#dddddd", highlightthickness=1, highlightbackground="#888888")
        self.enemy_en_canvas.pack(fill=tk.X, pady=(2, 4))

        self.enemy_stats_var = tk.StringVar()
        tk.Label(enemy_box, textvariable=self.enemy_stats_var, anchor="w", fg="#333333").pack(fill=tk.X)

        # 3. Painel de Ações + Inventário
        middle_frame = tk.Frame(self, padx=10, pady=6)
        middle_frame.pack(fill=tk.X)
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.columnconfigure(1, weight=1)

        actions_box = tk.LabelFrame(middle_frame, text="Ações de Combate", padx=10, pady=8)
        actions_box.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        combat_row = tk.Frame(actions_box)
        combat_row.pack(fill=tk.X, pady=(0, 6))

        self.btn_attack = tk.Button(
            combat_row, text="Ataque Básico", width=16, command=self._on_basic_attack
        )
        self.btn_attack.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_defend = tk.Button(
            combat_row, text="Defender", width=14, command=self._on_defend
        )
        self.btn_defend.pack(side=tk.LEFT)

        tk.Label(actions_box, text="Habilidades:", anchor="w").pack(fill=tk.X)
        self.abilities_frame = tk.Frame(actions_box)
        self.abilities_frame.pack(fill=tk.X, pady=(2, 8))

        camp_row = tk.Frame(actions_box)
        camp_row.pack(fill=tk.X)

        self.btn_rest = tk.Button(
            camp_row, text="Descansar", width=14, command=self._on_rest
        )
        self.btn_rest.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_next_enemy = tk.Button(
            camp_row, text="Próximo Inimigo", width=18, command=self._on_next_enemy
        )
        self.btn_next_enemy.pack(side=tk.LEFT)

        # Inventário
        inv_box = tk.LabelFrame(middle_frame, text="Inventário", padx=10, pady=8)
        inv_box.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        self.inventory_listbox = tk.Listbox(inv_box, height=5)
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.btn_use_item = tk.Button(
            inv_box, text="Usar Item Selecionado", command=self._on_use_item
        )
        self.btn_use_item.pack(fill=tk.X)

        # 4. Log de combate rolável
        log_box = tk.LabelFrame(self, text="Log de Combate", padx=10, pady=8)
        log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))

        self.log_text = scrolledtext.ScrolledText(log_box, state="disabled", wrap=tk.WORD, height=12)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Redesenha barras se a janela for redimensionada
        self.hero_hp_canvas.bind("<Configure>", lambda _e: self._refresh_bars())
        self.enemy_hp_canvas.bind("<Configure>", lambda _e: self._refresh_bars())

    def _log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def _draw_bar(self, canvas: tk.Canvas, current: int, maximum: int, color: str) -> None:
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1:
            width = 360
        if height <= 1:
            height = 18
        ratio = 0.0 if maximum <= 0 else max(0.0, min(1.0, current / maximum))
        fill_width = int(width * ratio)
        if fill_width > 0:
            canvas.create_rectangle(0, 0, fill_width, height, fill=color, outline="")

    def _refresh_bars(self) -> None:
        self._draw_bar(self.hero_hp_canvas, self.hero.getCurrentHp(), self.hero.getMaxHp(), "#2e8b57")
        self._draw_bar(self.hero_en_canvas, self.hero.getCurrentEnergy(), self.hero.getMaxEnergy(), "#1e6bd6")
        self._draw_bar(self.enemy_hp_canvas, self.enemy.getCurrentHp(), self.enemy.getMaxHp(), "#c93b3b")
        self._draw_bar(self.enemy_en_canvas, self.enemy.getCurrentEnergy(), self.enemy.getMaxEnergy(), "#7b4bb7")

    def _refresh_ui(self) -> None:
        stage_display = min(self.stage_index + 1, len(CAMPAIGN_BOSSES))
        self.campaign_info_var.set(
            f"Slot: {self.slot_name} | Estágio: {stage_display}/{len(CAMPAIGN_BOSSES)} | "
            f"Vitórias: {self.enemies_defeated} | XP: {self.hero.getXp()}/{self.hero.getXpToNext()}"
        )

        hero_def = " [DEFENDENDO]" if self.hero.isDefending() else ""
        self.hero_desc_var.set(self.hero.getRoleDescription() + hero_def)
        self.hero_hp_var.set(f"HP: {self.hero.getCurrentHp()} / {self.hero.getMaxHp()}")
        self.hero_en_var.set(f"Energia: {self.hero.getCurrentEnergy()} / {self.hero.getMaxEnergy()}")
        self.hero_stats_var.set(
            f"ATQ: {self.hero.getAttack()} | DEF: {self.hero.getDefense()} | VEL: {self.hero.getSpeed()}"
        )

        enemy_def = " [DEFENDENDO]" if self.enemy.isDefending() else ""
        self.enemy_desc_var.set(self.enemy.getRoleDescription() + enemy_def)
        self.enemy_hp_var.set(f"HP: {self.enemy.getCurrentHp()} / {self.enemy.getMaxHp()}")
        self.enemy_en_var.set(f"Energia: {self.enemy.getCurrentEnergy()} / {self.enemy.getMaxEnergy()}")
        self.enemy_stats_var.set(
            f"ATQ: {self.enemy.getAttack()} | DEF: {self.enemy.getDefense()} | VEL: {self.enemy.getSpeed()}"
        )

        self._refresh_bars()

        # Atualiza estado dos botões de combate/acampamento
        combat_state = tk.NORMAL if (self.in_combat and self.hero.isAlive() and self.enemy.isAlive()) else tk.DISABLED
        camp_state = tk.NORMAL if not self.in_combat else tk.DISABLED
        self.btn_attack.configure(state=combat_state)
        self.btn_defend.configure(state=combat_state)
        self.btn_use_item.configure(state=combat_state)
        self.btn_rest.configure(state=camp_state)
        self.btn_next_enemy.configure(state=camp_state)

        # Reconstrói botões de habilidades dinamicamente
        for btn in self._ability_buttons:
            btn.destroy()
        self._ability_buttons.clear()

        for ability in self.hero.getAbilities():
            cd = ability.getCurrentCooldown()
            status_txt = f"Recarga: {cd}t" if cd > 0 else f"Custo: {ability.getEnergyCost()}"
            label = f"{ability.getName()} ({status_txt})"
            can_use = (
                combat_state == tk.NORMAL
                and ability.isReady(self.hero.getCurrentEnergy())
                and self.hero.getLevel() >= ability.getRequiredLevel()
            )
            btn = tk.Button(
                self.abilities_frame,
                text=label,
                state=tk.NORMAL if can_use else tk.DISABLED,
                command=lambda ab=ability: self._on_use_ability(ab),
            )
            btn.pack(side=tk.LEFT, padx=(0, 6))
            self._ability_buttons.append(btn)

        # Atualiza inventário
        self.inventory_listbox.delete(0, tk.END)
        for item in self.hero.getInventory().getItems():
            self.inventory_listbox.insert(
                tk.END, f"{item.name} (x{item.count}) — {item.description}"
            )

    def _start_encounter(self, log_header: bool = True) -> None:
        self.turn = 1
        self.in_combat = True
        if log_header:
            self._log(f"\n>>> ENCONTRO INICIADO: {self.enemy.getRoleDescription()} <<<")
        self._begin_player_turn()

    def _begin_player_turn(self) -> None:
        self.hero.setDefending(False)
        for ability in self.hero.getAbilities():
            ability.tickCooldown()

        self._log(f"--- Turno {self.turn} ---")
        for msg in self.hero.applyTurnStartPassive():
            self._log(msg)
        self._refresh_ui()

    def _finish_player_action(self) -> None:
        if not self.enemy.isAlive():
            self._handle_victory()
            return

        # Turno do inimigo
        self.enemy.setDefending(False)
        for msg in self.enemy.applyTurnStartPassive():
            self._log(msg)

        if self.enemy.isAlive():
            ai_result = self.enemy.takeTurnAi(self.hero)
            self._log(f"[Inimigo] {ai_result.message}")

        if not self.hero.isAlive():
            self._handle_defeat()
            return

        self.turn += 1
        self._begin_player_turn()

    def _handle_victory(self) -> None:
        self.in_combat = False
        self.enemies_defeated += 1
        completed_before = self.stage_index >= len(CAMPAIGN_BOSSES)
        if not completed_before:
            self.stage_index += 1

        self._log(f"\nVITÓRIA! {self.hero.getName()} derrotou {self.enemy.getName()}!")
        prev_level = self.hero.getLevel()
        self.hero.gainXp(self.enemy.getXpReward())
        self._log(
            f"XP ganho: +{self.enemy.getXpReward()} "
            f"(XP atual: {self.hero.getXp()}/{self.hero.getXpToNext()})"
        )
        if self.hero.getLevel() > prev_level:
            self._log(
                f"LEVEL UP! {self.hero.getName()} subiu para o nível {self.hero.getLevel()}!"
            )

        loot_table = ["Néctar", "Elixir Olímpico", "Ambrosia"]
        reward_item = loot_table[(self.enemies_defeated - 1) % len(loot_table)]
        self.hero.getInventory().addItem(reward_item, 1)
        self._log(f"[Recompensa] Você recebeu 1x {reward_item}!")

        if self.stage_index == len(CAMPAIGN_BOSSES) and isinstance(self.enemy, TyphonBane):
            self._log("*** PARABÉNS! Você derrotou Tifão e concluiu a campanha! ***")

        self.save_manager.save_game(self.slot_name, self.hero, self.stage_index, self.enemies_defeated)
        self._log(f"[Auto-Save] Progresso salvo no slot '{self.slot_name}'.")
        self._log("Clique em 'Descansar' ou 'Próximo Inimigo' para continuar.")
        self._refresh_ui()

    def _handle_defeat(self) -> None:
        self.in_combat = False
        self._log(f"\nDERROTA! {self.hero.getName()} caiu diante de {self.enemy.getName()}...")
        self._log("Clique em 'Descansar' para recuperar suas forças e tentar novamente.")
        self._refresh_ui()

    def _on_basic_attack(self) -> None:
        if not self.in_combat:
            return
        dmg = self.hero.basicAttack(self.enemy)
        self._log(f"[Ataque] {self.hero.getName()} atacou {self.enemy.getName()} e causou {dmg} de dano!")
        self._finish_player_action()

    def _on_defend(self) -> None:
        if not self.in_combat:
            return
        self.hero.setDefending(True)
        self._log(f"[Defesa] {self.hero.getName()} assumiu postura defensiva!")
        self._finish_player_action()

    def _on_use_ability(self, ability) -> None:
        if not self.in_combat:
            return
        result = ability.execute(self.hero, self.enemy)
        self._log(f"[Habilidade] {result.message}")
        if result.success:
            self._finish_player_action()
        else:
            self._refresh_ui()

    def _on_use_item(self) -> None:
        if not self.in_combat:
            return
        selection = self.inventory_listbox.curselection()
        if not selection:
            messagebox.showinfo("Inventário", "Selecione um item na lista antes de usar.")
            return

        items = self.hero.getInventory().getItems()
        idx = int(selection[0])
        if idx >= len(items):
            return

        chosen_item = items[idx]
        if self.hero.getInventory().useItem(chosen_item.name, self.hero):
            self._log(f"[Item] {self.hero.getName()} usou {chosen_item.name}!")
            self._finish_player_action()
        else:
            messagebox.showwarning("Inventário", "Não foi possível usar o item selecionado.")

    def _on_rest(self) -> None:
        healed = self.hero.heal(self.hero.getMaxHp())
        if not self.hero.isAlive():
            # Caso venha de derrota, ressuscita no acampamento com HP e Energia cheios
            self.hero._current_hp = self.hero.getMaxHp()
            healed = self.hero.getMaxHp()
        energy = self.hero.restoreEnergy(self.hero.getMaxEnergy())
        for ability in self.hero.getAbilities():
            ability.setCurrentCooldown(0)
        self._log(f"[Acampamento] {self.hero.getName()} descansou (+{healed} HP, +{energy} Energia).")
        self._refresh_ui()

    def _on_next_enemy(self) -> None:
        if not self.hero.isAlive():
            self._on_rest()
        self.enemy = self._create_enemy_for_stage(self.stage_index)
        self._start_encounter(log_header=True)

    def _save_current_game(self) -> None:
        self.save_manager.save_game(self.slot_name, self.hero, self.stage_index, self.enemies_defeated)
        self._log(f"[Save] Progresso salvo no slot '{self.slot_name}'.")
        messagebox.showinfo("Salvar Jogo", f"Jogo salvo com sucesso no slot '{self.slot_name}'!")

    def _open_new_game_dialog(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Novo Jogo")
        dialog.geometry("380x270")
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="Nome do Semideus:").pack(anchor="w", padx=12, pady=(12, 2))
        name_var = tk.StringVar(value="Percy")
        tk.Entry(dialog, textvariable=name_var).pack(fill=tk.X, padx=12)

        tk.Label(dialog, text="Nome do Slot de Save:").pack(anchor="w", padx=12, pady=(8, 2))
        slot_var = tk.StringVar(value="aventura_2")
        tk.Entry(dialog, textvariable=slot_var).pack(fill=tk.X, padx=12)

        tk.Label(dialog, text="Escolha a Linhagem Divina:").pack(anchor="w", padx=12, pady=(10, 2))
        class_var = tk.StringVar(value="ChildOfZeus")
        for label, value in [
            ("Filho(a) de Zeus (Cargas Estáticas / Raio)", "ChildOfZeus"),
            ("Filho(a) de Poseidon (Regeneração / Onda)", "ChildOfPoseidon"),
            ("Filho(a) de Hades (Drenagem Vital / Sombras)", "ChildOfHades"),
        ]:
            tk.Radiobutton(dialog, text=label, variable=class_var, value=value).pack(
                anchor="w", padx=16
            )

        def confirm() -> None:
            hero_name = name_var.get().strip() or "Herói"
            slot = slot_var.get().strip() or hero_name.lower().replace(" ", "_")
            self.slot_name = slot
            self.stage_index = 0
            self.enemies_defeated = 0
            self.hero = self._build_default_hero(hero_name, class_var.get())
            self.enemy = self._create_enemy_for_stage(0)
            self.save_manager.save_game(self.slot_name, self.hero, self.stage_index, self.enemies_defeated)
            self._log(f"\n[Novo Jogo] {self.hero.getName()} ({class_var.get()}) criado no slot '{self.slot_name}'!")
            dialog.destroy()
            self._start_encounter(log_header=True)

        tk.Button(dialog, text="Iniciar Aventura", command=confirm).pack(pady=12)

    def _open_load_dialog(self) -> None:
        saves = self.save_manager.list_saves()
        if not saves:
            messagebox.showinfo("Carregar Jogo", "Nenhum jogo salvo encontrado no banco SQLite.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Carregar Jogo Salvo")
        dialog.geometry("500x300")
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="Selecione um save:").pack(anchor="w", padx=10, pady=(10, 4))
        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        def populate() -> None:
            listbox.delete(0, tk.END)
            for s in saves:
                listbox.insert(
                    tk.END,
                    f"[{s['slot_name']}] {s['hero_name']} ({s['hero_class']} Nv.{s['level']}) | "
                    f"HP {s['current_hp']}/{s['max_hp']} | Estágio {s['stage_index']}/5",
                )

        populate()

        btn_row = tk.Frame(dialog, pady=8)
        btn_row.pack()

        def load_selected() -> None:
            sel = listbox.curselection()
            if not sel:
                return
            chosen_slot = saves[int(sel[0])]["slot_name"]
            loaded = self.save_manager.load_game(chosen_slot)
            if loaded is None:
                messagebox.showerror("Erro", "Falha ao carregar o save selecionado.")
                return
            hero, stage_idx, defeated = loaded
            self.hero = hero
            self.slot_name = chosen_slot
            self.stage_index = stage_idx
            self.enemies_defeated = defeated
            self.enemy = self._create_enemy_for_stage(self.stage_index)
            self._log(f"\n[Load] Save '{chosen_slot}' carregado com sucesso!")
            dialog.destroy()
            self._start_encounter(log_header=True)

        def delete_selected() -> None:
            sel = listbox.curselection()
            if not sel:
                return
            idx = int(sel[0])
            chosen_slot = saves[idx]["slot_name"]
            if self.save_manager.delete_save(chosen_slot):
                saves.pop(idx)
                populate()
                self._log(f"[Save] Slot '{chosen_slot}' excluído.")

        tk.Button(btn_row, text="Carregar Selecionado", command=load_selected).pack(
            side=tk.LEFT, padx=6
        )
        tk.Button(btn_row, text="Excluir Selecionado", command=delete_selected).pack(
            side=tk.LEFT, padx=6
        )
        tk.Button(btn_row, text="Fechar", command=dialog.destroy).pack(side=tk.LEFT, padx=6)
