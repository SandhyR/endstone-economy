from endstone.command import Command, CommandSender, CommandExecutor


class SetMoney(CommandExecutor):
    def __init__(self, economy):
        super().__init__()
        self.receiver = None
        self.money = None
        self.sender = None
        self.economy = economy

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        self.sender = sender
        if len(args) >= 2:
            self.receiver = args[0]
            self.money = args[1]
            self.economy.dbmanager.update_player_money(obj=self, name=self.receiver.lower(), money=self.money,
                                                     callback=self.handle_update)
            return True
        else:
            return False



    def handle_update(obj, self, result):
        if result:
            self.sender.send_message(f"Successfully updated {self.receiver} money to {self.money}")
        else:
            self.sender.send_message("Player not found or error occurred")
