from endstone.command import Command, CommandSender, CommandExecutor


class SeeMoney(CommandExecutor):
    def __init__(self, economy):
        super().__init__()
        self.sender = None
        self.economy = economy

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        self.sender = sender
        self.target = args[0]
        if len(args) >= 1:
            self.economy.dbmanager.read_player_money(obj=self, name=self.target.lower(),
                                                     callback=self.handle_player_money_result)
        return True

    def handle_player_money_result(obj, self, result):
        if result is not None:
            self.sender.send_message(f"{self.target} money is {result}")
        else:
            self.sender.send_message("Player not found or error occurred")
