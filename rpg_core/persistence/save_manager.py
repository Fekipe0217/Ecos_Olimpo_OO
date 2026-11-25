from datetime import datetime
import sqlite3

from rpg_core.abilities.ability import Ability
from rpg_core.abilities.shadow_strike import ShadowStrike
from rpg_core.abilities.thunderbolt import Thunderbolt
from rpg_core.abilities.tidal_surge import TidalSurge
from rpg_core.characters.child_of_hades import ChildOfHades
from rpg_core.characters.child_of_poseidon import ChildOfPoseidon
from rpg_core.characters.child_of_zeus import ChildOfZeus
from rpg_core.characters.demigod import Demigod


HERO_CLASSES: dict[str, type[Demigod]] = {
    "ChildOfZeus": ChildOfZeus,
    "ChildOfPoseidon": ChildOfPoseidon,
    "ChildOfHades": ChildOfHades,
}

ABILITY_CLASSES: dict[str, type[Ability]] = {
    "Thunderbolt": Thunderbolt,
    "TidalSurge": TidalSurge,
    "ShadowStrike": ShadowStrike,
}


class SaveManager:
    """Gerencia a persistência de progresso do jogador usando SQLite nativo (sqlite3)."""

    def __init__(self, db_path: str = "rpg_saves.db") -> None:
        self._db_path = db_path
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """Cria as tabelas de saves, inventário e habilidades caso ainda não existam."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS saves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slot_name TEXT UNIQUE NOT NULL,
                    hero_class TEXT NOT NULL,
                    hero_name TEXT NOT NULL,
                    level INTEGER NOT NULL,
                    xp INTEGER NOT NULL,
                    xp_to_next INTEGER NOT NULL,
                    max_hp INTEGER NOT NULL,
                    current_hp INTEGER NOT NULL,
                    max_energy INTEGER NOT NULL,
                    current_energy INTEGER NOT NULL,
                    attack INTEGER NOT NULL,
                    defense INTEGER NOT NULL,
                    speed INTEGER NOT NULL,
                    static_charges INTEGER NOT NULL DEFAULT 0,
                    stage_index INTEGER NOT NULL DEFAULT 0,
                    enemies_defeated INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS save_inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    save_id INTEGER NOT NULL,
                    item_name TEXT NOT NULL,
                    count INTEGER NOT NULL,
                    FOREIGN KEY (save_id) REFERENCES saves(id) ON DELETE CASCADE
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS save_abilities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    save_id INTEGER NOT NULL,
                    ability_class TEXT NOT NULL,
                    current_cooldown INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (save_id) REFERENCES saves(id) ON DELETE CASCADE
                );
                """
            )

    def save_game(
        self,
        slot_name: str,
        hero: Demigod,
        stage_index: int,
        enemies_defeated: int,
    ) -> None:
        """Salva ou sobrescreve o progresso completo do jogador no slot informado."""
        hero_class_name = type(hero).__name__
        static_charges = hero.getStaticCharges() if isinstance(hero, ChildOfZeus) else 0
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO saves (
                    slot_name, hero_class, hero_name, level, xp, xp_to_next,
                    max_hp, current_hp, max_energy, current_energy,
                    attack, defense, speed, static_charges,
                    stage_index, enemies_defeated, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(slot_name) DO UPDATE SET
                    hero_class = excluded.hero_class,
                    hero_name = excluded.hero_name,
                    level = excluded.level,
                    xp = excluded.xp,
                    xp_to_next = excluded.xp_to_next,
                    max_hp = excluded.max_hp,
                    current_hp = excluded.current_hp,
                    max_energy = excluded.max_energy,
                    current_energy = excluded.current_energy,
                    attack = excluded.attack,
                    defense = excluded.defense,
                    speed = excluded.speed,
                    static_charges = excluded.static_charges,
                    stage_index = excluded.stage_index,
                    enemies_defeated = excluded.enemies_defeated,
                    updated_at = excluded.updated_at;
                """,
                (
                    slot_name,
                    hero_class_name,
                    hero.getName(),
                    hero.getLevel(),
                    hero.getXp(),
                    hero.getXpToNext(),
                    hero.getMaxHp(),
                    hero.getCurrentHp(),
                    hero.getMaxEnergy(),
                    hero.getCurrentEnergy(),
                    hero.getAttack(),
                    hero.getDefense(),
                    hero.getSpeed(),
                    static_charges,
                    stage_index,
                    enemies_defeated,
                    updated_at,
                ),
            )

            row = conn.execute(
                "SELECT id FROM saves WHERE slot_name = ?;", (slot_name,)
            ).fetchone()
            save_id = int(row["id"])

            conn.execute("DELETE FROM save_inventory WHERE save_id = ?;", (save_id,))
            for item in hero.getInventory().getItems():
                conn.execute(
                    "INSERT INTO save_inventory (save_id, item_name, count) VALUES (?, ?, ?);",
                    (save_id, item.name, item.count),
                )

            conn.execute("DELETE FROM save_abilities WHERE save_id = ?;", (save_id,))
            for ability in hero.getAbilities():
                conn.execute(
                    "INSERT INTO save_abilities (save_id, ability_class, current_cooldown) VALUES (?, ?, ?);",
                    (save_id, type(ability).__name__, ability.getCurrentCooldown()),
                )

    def list_saves(self) -> list[dict]:
        """Lista todos os jogos salvos ordenados pela atualização mais recente."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT slot_name, hero_class, hero_name, level, current_hp, max_hp,
                       stage_index, enemies_defeated, updated_at
                FROM saves
                ORDER BY updated_at DESC, id DESC;
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def load_game(self, slot_name: str) -> tuple[Demigod, int, int] | None:
        """Reconstrói o herói, inventário, habilidades e estágio a partir do SQLite."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM saves WHERE slot_name = ?;", (slot_name,)
            ).fetchone()
            if row is None:
                return None

            hero_cls = HERO_CLASSES.get(row["hero_class"])
            if hero_cls is None:
                return None

            hero = hero_cls(name=row["hero_name"])
            hero.restoreState(
                level=int(row["level"]),
                xp=int(row["xp"]),
                xp_to_next=int(row["xp_to_next"]),
                max_hp=int(row["max_hp"]),
                current_hp=int(row["current_hp"]),
                max_energy=int(row["max_energy"]),
                current_energy=int(row["current_energy"]),
                attack=int(row["attack"]),
                defense=int(row["defense"]),
                speed=int(row["speed"]),
            )
            if isinstance(hero, ChildOfZeus):
                hero.setStaticCharges(int(row["static_charges"]))

            save_id = int(row["id"])

            inv_rows = conn.execute(
                "SELECT item_name, count FROM save_inventory WHERE save_id = ?;",
                (save_id,),
            ).fetchall()
            for inv in inv_rows:
                hero.getInventory().addItem(str(inv["item_name"]), int(inv["count"]))

            hero.clearAbilities()
            ab_rows = conn.execute(
                "SELECT ability_class, current_cooldown FROM save_abilities WHERE save_id = ?;",
                (save_id,),
            ).fetchall()
            for ab in ab_rows:
                ab_cls = ABILITY_CLASSES.get(str(ab["ability_class"]))
                if ab_cls is not None:
                    ability = ab_cls()
                    ability.setCurrentCooldown(int(ab["current_cooldown"]))
                    hero.addAbility(ability)

            return hero, int(row["stage_index"]), int(row["enemies_defeated"])

    def delete_save(self, slot_name: str) -> bool:
        """Remove um jogo salvo pelo nome do slot."""
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM saves WHERE slot_name = ?;", (slot_name,))
            return cur.rowcount > 0
