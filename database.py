import sqlite3
DB_PATH = "game.db"


def get_or_create_player(name: str):
    if not (2 <= len(name) <= 20) or not name.replace(" ", "").isalpha():
        raise ValueError("Имя должно содержать только буквы и быть от 2 до 20 символов.")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM players WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            cursor.execute("INSERT INTO players (name) VALUES (?)", (name,))
            return cursor.lastrowid


def is_level_completed(player_id: int, level_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT completed FROM progress WHERE player_id = ? AND level_id = ?",
                       (player_id, level_id))
        row = cursor.fetchone()
        return bool(row[0]) if row else False


def unlock_level(player_id: int, level_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE progress 
            SET completed = 1 
            WHERE player_id = ? AND level_id = ?""", (player_id, level_id))
        if cursor.rowcount == 0:
            cursor.execute("""INSERT INTO progress (player_id, level_id, completed)
                VALUES (?, ?, 1)""", (player_id, level_id))