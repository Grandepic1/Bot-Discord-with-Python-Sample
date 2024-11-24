# Discord Bot Project

Welcome to the **Discord Bot Project**, a Python-based bot designed to enhance your Discord server with a variety of powerful and user-friendly commands. This bot is built using the [Discord Python API]([https://discord.com/developers/docs/intro](https://discordpy.readthedocs.io/en/stable/api.html)), enabling seamless integration and customization.

---

## Features

This bot provides an extensive suite of commands organized into three distinct categories:

### 1. Information Commands (`info`)
These commands provide server or user-related information to enhance your server's engagement and functionality.
- **Examples:**
  - Display user information.
  - Show server statistics.
  - Fetch role details.

### 2. Moderation Commands (`moderation`)
Aimed at server administrators, these commands help maintain order and manage the server efficiently.
- **Examples:**
  - Kick or ban users.
  - Mute or unmute members.
  - Clear chat messages in bulk.

### 3. Owner Commands (`owner`)
Restricted to the bot owner, these commands are designed for advanced bot management and debugging purposes.
- **Examples:**
  - Reload bot configurations.
  - Manage command availability.
  - Execute administrative-level tasks.

---

## Getting Started

Follow the steps below to set up and run the bot in your server:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

### 2. Install Dependencies
Ensure you have Python installed (version 3.8 or higher). Install the required packages using:
```bash
pip install -r requirements.txt
```

### 3. Edit Environment Variables
Edit file .env based on your using:
```env
TOKEN="put your bot id here"
PREFIX=!
MUTE-ROLE=put your mute role here
```

### 4. Run The Bot
```bash
python main.py
```
The bot will connect to Discord and become operational in your server.

## Usage

1. **Invite the bot to your server.**
2. **Use commands via the bot's prefix** (e.g., `!`, `$`, or `/` depending on your configuration).
3. Access the following categories based on your permissions:

| Command Category | Access Level                | Example Commands       |
|-------------------|-----------------------------|-------------------------|
| **Info**          | All members                | `!userinfo`, `!server` |
| **Moderation**    | Server moderators/admins   | `!ban`, `!mute`        |
| **Owner**         | Bot owner only             | `!reload`, `!eval`     |

---

## Customization

You can customize the bot’s functionality by modifying the `commands` directory. Each category of commands is located in a separate module, making it easy to add or remove features.

- **Info Commands**: `commands/Info.py`
- **Moderation Commands**: `commands/moderation.py`
- **Owner Commands**: `commands/owner.py`

---

## API Reference

This bot uses the [Discord API](https://discord.com/developers/docs/intro) to interact with the Discord platform. Key features include:
- Handling events like messages, reactions, and member updates.
- Managing server roles, channels, and permissions.
- Interacting with users via commands and responses.

Learn more about the Discord API in the [official documentation](https://discord.com/developers/docs/intro).

---


## License

This project is open-source and licensed under the [MIT License](LICENSE). Feel free to use.

---

## Contact
This project is still on running.
If you have questions or feedback, feel free to reach out:
- Discord: `grandepic1`
- Email: `revaldo652@gmail.com`

---

Happy coding, and enjoy managing your server with your customized Discord bot! 🎉