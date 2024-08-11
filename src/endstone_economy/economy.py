
from endstone._internal.endstone_python import PlayerJoinEvent
from endstone.event import event_handler
from endstone.plugin import Plugin
from endstone_economy.cmd.mymoney import MyMoney

from endstone_economy.cmd.pay import Pay
from endstone_economy.cmd.seemoney import SeeMoney
from endstone_economy.cmd.setmoney import SetMoney
from endstone_economy.dbmanager import DBManager, MySQLDBManager, SQLiteDBManager


class Economy(Plugin):
    name = "economy"
    version = "0.1.0"
    api_version = "0.5"
    description = "Economy plugin"
    commands = {
        "mymoney": {
            "description": "Get your money count",
            "usages": ["/mymoney"],
            "permissions": ["economy.command.general"]
        },
        "setmoney": {
            "description": "Set your money count",
            "usages": ["/setmoney [player: str] [amount: int]"],
            "permissions": ["economy.command.admin"]
        },
        "pay": {
            "description": "Pay money to another player",
            "usages": ["/pay [player: str] [amount: int]"],
            "permissions": ["economy.command.general"]
        },
        "seemoney": {
            "description": "See another player's money count",
            "usages": ["/seemoney [player: str]"],
            "permissions": ["economy.command.general"]
        }
    }

    permissions = {
        "economy.command.general": {
            "description": "General economy commands",
            "default": "true",
        },
        "economy.command.admin": {
            "description": "Admin economy commands",
            "default": "op",
        },
    }

    startermoney = 0

    def __init__(self):
        super().__init__()
        self.database = None
        self.dbmanager = None

    def on_load(self) -> None:
        self.logger.info("Economy Plugin Loaded")

    def on_enable(self) -> None:
        self.logger.info("Economy Plugin Activated")
        self.save_default_config()
        self.load_config()
        if self.database.lower() == "mysql":
            self.dbmanager = MySQLDBManager(self.config["mysql"])
        else:
            self.dbmanager = SQLiteDBManager(self.config["sqlite"])
        self.dbmanager.setup_database()
        self.get_command("mymoney").executor = MyMoney(self)
        self.get_command("pay").executor = Pay(self)
        self.get_command("seemoney").executor = SeeMoney(self)
        self.get_command("setmoney").executor = SetMoney(self)
        self.register_events(self)

    def on_disable(self) -> None:
        self.logger.info("Economy Plugin Disabled")
        self.dbmanager.close()

    def load_config(self) -> None:
        self.startermoney = self.config["economy"]["starter-money"]
        self.database = self.config["database"]["db"]


    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        self.dbmanager.create_player(event.player.name.lower(), event.player.xuid, self.startermoney)
