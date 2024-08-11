from concurrent.futures import ThreadPoolExecutor
import mysql.connector
import sqlite3


class DBManager:
    def __init__(self,  credentials: dict[str]):
        super().__init__()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def create_player(self, player_name: str, xuid: str, money: int) -> None:
        self.executor.submit(self._create_player, player_name, xuid, money)

    def read_player_money(self, obj, name: str, callback=None):
        future = self.executor.submit(self._read_player_money, name)
        if callback:
            future.add_done_callback(lambda fut: callback(obj, fut.result()))

    def update_player_money(self, obj, name: str, money: int, callback=None) -> None:
        future = self.executor.submit(self._update_player_money, name, money)
        if callback:
            future.add_done_callback(lambda fut: callback(obj, fut.result()))

    def increase_player_money(self, name: str, money: int, obj, callback=None) -> None:
        future = self.executor.submit(self._increase_player_money, name, money)
        if callback:
            future.add_done_callback(lambda fut: callback(obj, fut.result()))

    def decrease_player_money(self, name: str, money: int, obj, callback=None) -> None:
        future = self.executor.submit(self._decrease_player_money, name, money)
        if callback:
            future.add_done_callback(lambda fut: callback(obj, fut.result()))

    def delete_player(self, name: str) -> None:
        self.executor.submit(self._delete_player, name)

    def _create_player(self, player_name: str, xuid: str, money: int) -> None:
        raise NotImplementedError

    def _read_player_money(self, name: str):
        raise NotImplementedError

    def _update_player_money(self, name: str, money: int) -> bool:
        raise NotImplementedError

    def _increase_player_money(self, name: str, money: int) -> bool:
        raise NotImplementedError

    def _decrease_player_money(self, name: str, money: int) -> bool:
        raise NotImplementedError

    def _delete_player(self, name: str) -> None:
        raise NotImplementedError

    def run_query(self, query: str, values: tuple = ()):
        raise NotImplementedError

    def setup_database(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class MySQLDBManager(DBManager):
    def __init__(self, credentials: dict[str]):
        super().__init__(credentials)
        self.mydb = mysql.connector.connect(
            host=credentials["host"],
            user=credentials["user"],
            password=credentials["password"],
            database=credentials["database"]
        )
        self.cursor = self.mydb.cursor()

    def _create_player(self, player_name: str, xuid: str, money: int) -> None:
        query = "INSERT INTO economy (player_name, xuid, money) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE player_name=VALUES(player_name)"
        values = (player_name, xuid, money)
        self.run_query(query, values)

    def _read_player_money(self, name: str):
        query = "SELECT money FROM economy WHERE player_name = %s"
        cursor = self.cursor
        try:
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return only the money value
            else:
                return None
        except Exception as e:
            # self.logger.error(f"Database error: {e}")
            return None

    def _update_player_money(self, name: str, money: int) -> bool:
        query = "UPDATE economy SET money = %s WHERE player_name = %s"
        values = (money, name)
        return self.run_query(query, values)

    def _increase_player_money(self, name: str, money: int) -> bool:
        query = "UPDATE economy SET money = money + %s WHERE player_name = %s"
        values = (money, name)
        return self.run_query(query, values)

    def _decrease_player_money(self, name: str, money: int) -> bool:
        query = "UPDATE economy SET money = money - %s WHERE player_name = %s"
        values = (money, name)
        return self.run_query(query, values)

    def _delete_player(self, name: str) -> None:
        query = "DELETE FROM economy WHERE player_name = %s"
        values = (name,)
        self.run_query(query, values)

    def run_query(self, query: str, values: tuple = ()):
        self.cursor.execute(query, values)
        self.mydb.commit()
        if self.cursor.rowcount == 0:
            return False
        return True

    def setup_database(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS economy (id INT AUTO_INCREMENT PRIMARY KEY, player_name VARCHAR(50) NOT NULL, xuid VARCHAR(20) NOT NULL, money INT DEFAULT 0 CHECK (money >= 0), UNIQUE KEY (xuid))")

    def close(self):
        self.cursor.close()
        self.mydb.close()
        self.executor.shutdown()


class SQLiteDBManager(DBManager):
    def __init__(self, credentials: dict[str]):
        super().__init__(credentials)
        self.mydb = sqlite3.connect(credentials["path"], check_same_thread=False)
        self.cursor = self.mydb.cursor()


    def _create_player(self, player_name: str, xuid: str, money: int) -> None:
        query = "INSERT OR IGNORE INTO economy (player_name, xuid, money) VALUES (?, ?, ?) ON CONFLICT(xuid) DO UPDATE SET player_name=excluded.player_name"
        values = (player_name, xuid, money)
        self.run_query(query, values)

    def _read_player_money(self, name: str):
        query = "SELECT money FROM economy WHERE player_name = ?"
        values = (name,)
        cursor = self.cursor
        try:
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return only the money value
            else:
                return None
        except Exception as e:
            # self.logger.error(f"Database error: {e}")
            return None

    def _update_player_money(self, name: str, money: int) -> bool:
        query = "UPDATE economy SET money = ? WHERE player_name = ?"
        values = (money, name)
        return self.run_query(query, values)

    def _increase_player_money(self, name: str, money: int) -> bool:
        query = "UPDATE economy SET money = money + ? WHERE player_name = ?"
        values = (money, name)
        return self.run_query(query, values)

    def _decrease_player_money(self, name: str, money: int) -> bool:
        query = "UPDATE economy SET money = money - ? WHERE player_name = ?"
        values = (money, name)
        return self.run_query(query, values)

    def _delete_player(self, name: str) -> None:
        query = "DELETE FROM economy WHERE player_name = ?"
        values = (name,)
        self.run_query(query, values)

    def run_query(self, query: str, values: tuple = ()):
        self.cursor.execute(query, values)
        self.mydb.commit()
        if self.cursor.rowcount == 0:
            return False
        return True

    def setup_database(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS economy (id INTEGER PRIMARY KEY AUTOINCREMENT, player_name TEXT NOT NULL, xuid TEXT NOT NULL, money INTEGER DEFAULT 0 CHECK (money >= 0), UNIQUE(xuid))")

    def close(self):
        self.cursor.close()
        self.mydb.close()
        self.executor.shutdown()
