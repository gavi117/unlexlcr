# Chatty Bot README

## 🦉 Overview

**Chatty Bot** is a versatile and user-friendly Discord bot designed to provide a variety of helpful and entertaining features for your community. It supports both prefix and slash commands, offers scheduled automation, and always stays up-to-date with an informative versioning system.

## Main Features

- **Slash Commands** (officially registered and convenient for users)
- **Prefix Commands** for admins & quick actions
- **Daily Mission Automations** with in-server scheduling
- **Rich Version/Changelog Info** available via commands
- **Timezone Utility Tools**
- **Admin List Generator** from text data
- **Fun Dice Roller**
- Modular, maintainable, and fully async

## Setup & Requirements

- Python 3.8+
- Discord bot token in the environment variable `DISCORD_TOKEN`
- [discord.py (v2.3+ recommended)](https://discordpy.readthedocs.io/)
- `apscheduler` package for scheduled tasks
- The `keep_alive` module for uptime monitoring (recommended for render.com deployments)

## Getting Started

1. **Clone the repository and install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Set environment variable:**

    - On your hosting platform (Render, Replit, etc.), set a secret ENV variable named `DISCORD_TOKEN` with your bot token.

3. **Run the bot:**

    ```bash
    python bot.py
    ```

4. **Invite the bot:**  
    Make sure to select scopes for:
    - `applications.commands`
    - `bot`
    - and enable the `MESSAGE CONTENT INTENT` for full feature support.

## Slash Commands

| Command                 | Description                                                       | Scope             |
|-------------------------|-------------------------------------------------------------------|-------------------|
| **/about**              | Shows bot info, version, and catchphrase.                         | Global            |
| **/version**            | Shows a summary of the latest version update.                     | Admin Guilds      |
| **/versioninfo [ver]**  | Detailed changelog for specified version.                         | Admin Guilds      |
| **/versionlog**         | List of all released versions and top features.                   | Admin Guilds      |
| **/ntime [tz]**         | Shows current time in a specified timezone (ex: +9, -5, 09:00).   | Global            |
| **/dailytasks**         | Shows today's SIS daily missions (uses Moscow time).              | Admin Guilds      |
| **/dice [sides]**       | Rolls a dice [default: 6 sides; custom: 1-N].                     | Global            |

## Prefix Commands

| Command                 | Description                                                                                   |
|-------------------------|-----------------------------------------------------------------------------------------------|
| `/adminlist`            | Generates an admin rank-ordered list. Paste your admin roster or upload a `.txt` for result.  |

## Scheduler

- Uses **APScheduler** to send daily task messages at 06:00 MSK to a specific channel.  
- This is useful for automatic daily missions or reminders.

## Version History

### Latest version: `1.2.2`

#### Previous Changelog Highlights

- Modular redesign using **Cog architecture**
- Unified slash/prefix command handling
- Enhanced timezone utilities (UTC+1, UTC+3, UTC+9, custom offset support)
- Scheduled task automation for daily operations
- Adminlist parser for roster processing via message/attachment

*Versions marked Beta are for internal/testing use only.*

## Guild/Channel Setup

- The bot uses **guild whitelisting** for admin-specific commands.  
- Make sure to update `ALL_GUILD_IDS` and `ADMIN_GUILD_IDS` to your guild/server IDs.
- Daily task messages use a hardcoded channel ID—update as necessary for your environment!

## Customization

1. **Daily Tasks**:  
   Edit `WEEKLY_TASKS` in the code for your own community's recurring assignments.
2. **Guilds**:  
   Update your server IDs in the code blocks for `ALL_GUILD_IDS` and `ADMIN_GUILD_IDS`.
3. **Message/Presence**:  
   Adjust the bot's status message or scheduled time as you prefer in the code.

## Deployment Tips

- For continuous uptime (esp. on free hosts), use a webserver ping (see `keep_alive.py`).
- To enable slash command registration in all guilds, consider syncing on every `on_ready`.

## Example: /dailytasks Output

```
:detective: Greetings SIS Director, 
# :clipboard:  Today's Missions
-# 22 July 2025
1. Do Any Event with Your Members
2. Patrol YPD and Check
3. Conduct 1 Interview
**Have a good day! :muscle: :sparkles: **
-# Just a reminder to submit the Curator Task Report by 23:59 server time today. You can pass on some of the tasks to Deputies or other Senior Staff if needed.
```

## Advanced: Custom Slash Commands

- The commands are built using `discord.app_commands` and new-style slash command decorators.
- You can easily extend functionality by following the command templates and updating the version changelog.

## Contributing

1. Fork and submit a PR!
2. Follow PEP8, use async, and update the version info for each change.

## License

MIT License.  
Feel free to use, modify, and deploy for both private and public Discord communities.