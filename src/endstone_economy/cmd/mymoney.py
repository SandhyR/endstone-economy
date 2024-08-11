from endstone.command import Command, CommandSender, CommandExecutor


class MyMoney(CommandExecutor):
    def __init__(self, economy):
        super().__init__()
        self.sender = None
        self.economy = economy

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        self.sender = sender
        self.economy.dbmanager.read_player_money(obj=self, name=sender.name.lower(),
                                                 callback=self.handle_player_money_result)
        return True

    def handle_player_money_result(obj, self, result):
        if result is not None:
            self.sender.send_message(f"Your money is {result}")
        else:
            self.sender.send_message("Player not found or error occurred")
