from endstone import Player
from endstone.command import Command, CommandSender, CommandExecutor


class Pay(CommandExecutor):
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
            if sender.name.lower() == self.receiver.lower():
                sender.send_message("You cannot transfer to your own account")
                return False
            self.economy.dbmanager.read_player_money(obj=self, name=sender.name.lower(),
                                                     callback=self.handle_money)
            return True
        else:
            return False



    def handle_increase(obj, self, result):
        if result:
            self.economy.dbmanager.decrease_player_money(name=self.sender.name.lower(), money=self.money, obj=self,
                                                         callback=self.handle_decrease)
        else:
            self.sender.send_message("Player not found or error occurred")

    def handle_decrease(obj, self, result):
        if result:
            receiver = self.receiver
            money = self.money
            self.sender.send_message(f"You transferred {money} to {receiver}")
        else:
            self.sender.send_message("error occurred")

    def handle_money(obj, self, result):
        if result >= int(self.money):
            self.economy.dbmanager.increase_player_money(name=self.receiver.lower(), money=self.money, obj=self,
                                                         callback=self.handle_increase)
        else:
            self.sender.send_message("You dont have enough money")
