# Endstone Economy


The Endstone Economy Plugin is a Minecraft Bedrock server plugin designed to manage an economy system within the game. The plugin allows players to manage their in-game money, facilitating commands like checking balance, setting balance, paying other players, and viewing other players' balances.

## Features
- **Create Player Account**: Automatically creates an account for new players joining the server.
- **Manage Player Money**: Players can check their money, set their money, pay other players, and view other players' money.
- **Database Support**: The plugin supports both MySQL and SQLite databases to store player economy data.
- **Multithreaded Operations**: The plugin uses threading to handle database operations asynchronously, preventing server lag.

## Usage
**The plugin provides several commands for managing the in-game economy:**

- **/mymoney** - Check your current balance.
- **/setmoney <amount>** - Set your balance to a specific amount.
- **/pay <player> <amount>** - Pay another player a specific amount.
- **/seemoney <player>** - View another player's balance.
