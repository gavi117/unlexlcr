# --- General settings ---
import discord
import os
import re #scmd#2
import io #pcmd#1
import asyncio #pcmd#1
import random
import calendar

# --- settings for Render ---
from keep_alive import keep_alive

# --- additional from ---
from discord import app_commands
from typing import Optional #versioninfo
from datetime import datetime, timedelta, timezone #scmd#2
from discord.ext import commands #pcmd#1
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- Version ---
VERSION_CHANGELOG = {
    "1.0.0": {
        "core": [
            "Initial release: Bot reacts to every message with a 👍 emoji."
        ]
    },
    "1.0.1": {
        "core": [
            "Ignore messages from the bot itself to avoid self-reactions.",
            "Enabled `message_content` intent to read message content as required by Discord.",
            "Added debug print to check DISCORD_TOKEN environment variable."
        ]
    },
    "1.1.0": {
        "prefix_commands": [
            "Added `/chatty_adminlist` to generate an admin list based on message content."
        ]
    },
    "1.1.1": {
        "slash_commands": [
            "Introduced an early version of `/timezones` slash command to display times in UTC+1 and UTC+3."
        ],
        "bugfixes": [
            "Improved consistency and format of date/time display."
        ]
    },
    "1.1.2": {
        "slash_commands": [
            "Added `/dailytask` to show SIS daily missions based on the current weekday.",
            "Enhanced `/timezones` to support UTC+9 display and better formatting."
        ],
        "scheduler": [
            "Implemented daily scheduled messages at 12:00 using APScheduler."
        ],
        "infra": [
            "Integrated `CommandTree` to support slash commands officially."
        ]
    },
    "1.1.3": {
        "slash_commands": [
            "Added a new `/dice` slash command with support for custom sides (1 to N)."
        ],
        "infra": [
            "Minimized intents usage for a lighter bot footprint.",
            "Introduced Cog-based architecture for modular command definitions."
        ]
    },
    "1.2.0": {
        "refactor": [
            "Rebuilt bot using `commands.Bot` for better command management.",
            "Unified command handling between prefix and slash commands."
        ],
        "slash_commands": [
            "Formally added `/dice`, `/ntime` (custom timezone), and `/dailytasks` as slash commands with proper guild filtering."
        ],
        "prefix_commands": [
            "Restricted `/chatty_adminlist` access to authorized guilds."
        ],
        "infra": [
            "Automated command sync for multiple guild IDs.",
            "Bot presence now shows current version with status message."
        ]
    },
    "1.2.1": {
        "slash_commands": [
            "Added `/about` to display bot version, description, and updates.",
            "Improved `/dice` to send initial message before showing result (more dynamic)."
        ],
        "refactor": [
            "Restructured version handling, GUILD constants and bot setup for consistency."
        ],
        "bugfixes": [
            "Cleaned up conflicts between prefix and slash commands for better stability."
        ]
    }
}
BETA_VERSIONS = ["1.2.1"]
RELEASED_VERSION = "1.2.2"

# --- GUILD setting ---
Official_Guild = 1395455459426570421
ADMIN_Guild = 1369795873630064640
SV_01_Guild = 1320276107517362228 #SIS
SV_04_Guild = 1379346820509208616 #MU
SV_07_Guild = 1391512878707773491 #SIS

ADMIN_GUILD_IDS = [ADMIN_Guild, SV_01_Guild, SV_04_Guild, SV_07_Guild]
ADMIN_GUILD = [discord.Object(id=guild_id) for guild_id in ADMIN_GUILD_IDS]

ALL_GUILD_IDS = [Official_Guild, ADMIN_Guild, SV_01_Guild, SV_04_Guild, SV_07_Guild]
ALL_GUILD = [discord.Object(id=guild_id) for guild_id in ALL_GUILD_IDS]


# --- Discord setting ---
intents = discord.Intents.default()
intents.message_content = True  #enable message reading

bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

# --- timezone setting ---
MSK = timezone(timedelta(hours=3))

# -------------- slash-commands -------------- 
# ---------- version cmds ----------

CATEGORY_TITLES = {
    "core": "🔧 Core Features",
    "slash_commands": "🚀 Slash Commands",
    "prefix_commands": "💬 Prefix Commands",
    "scheduler": "⏰ Scheduled Jobs / Events",
    "infra": "⚙️ Infrastructure",
    "bugfixes": "🐞 Bug Fixes",
    "refactor": "💡 Refactor / Improvements"
}

# ----- version / version
# --- @ ---
@tree.command(
    name="version", 
    description="Show latest version update summary.",
    guilds=ADMIN_GUILD
)
async def version_command(interaction: discord.Interaction):
    version = RELEASED_VERSION
    changelog = VERSION_CHANGELOG.get(version)
    if not changelog:
        return await interaction.response.send_message(f"No info found for version {version}", ephemeral=True)

    content = f"📌 **Latest Version: v{version}**\n"
    for category, items in changelog.items():
        title = CATEGORY_TITLES.get(category, category.title())
        content += f"\n__**{title}**__\n"
        for item in items:
            content += f"- {item}\n"

    await interaction.response.send_message(content, ephemeral=True)

# ----- version / versioninfo
# --- @ ---
@tree.command(
    name="versioninfo",
    description="Show details of a specific version (default: latest released version).",
    guilds=ADMIN_GUILD
)
@app_commands.describe(version="Version number like 1.2.0 | default: latest")
async def versioninfo_command(interaction: discord.Interaction, version: Optional[str] = None):
    # If no input, fallback to the latest released version
    if version is None or version.lower() == "latest":
        version = RELEASED_VERSION

    changelog = VERSION_CHANGELOG.get(version)
    is_beta = version in BETA_VERSIONS

    if not changelog:
        return await interaction.response.send_message(f"❌ No changelog found for version `{version}`", ephemeral=True)

    content = f"📝 **Changelog for v{version}**"
    if is_beta:
        content += " ⚠️ **(Beta Version)**"
    content += "\n"

    for category, items in changelog.items():
        title = CATEGORY_TITLES.get(category, category.title())
        content += f"\n__**{title}**__\n"
        for item in items:
            content += f"- {item}\n"

    await interaction.response.send_message(content, ephemeral=True)

# ----- version / versionlog
# --- @ ---
@tree.command(
    name="versionlog", 
    description="Show a list of all past versions.",
    guilds=ADMIN_GUILD
)
async def versionlog_command(interaction: discord.Interaction):
    versions = sorted(VERSION_CHANGELOG.keys(), reverse=True)
    content = "**📚 Version History (Summary)**\n"

    for version in versions:
        changelog = VERSION_CHANGELOG[version]
        first_category = next(iter(changelog))
        first_summary = changelog[first_category][0]
        beta_mark = " ⚠️ (Beta)" if version in BETA_VERSIONS else ""
        content += f"- **v{version}**{beta_mark}: {first_summary}\n"

    await interaction.response.send_message(content, ephemeral=True)

# ---------- normal cmds ----------
# ----- scmd#1 / about
# --- @ ---
@tree.command(
    name="about",
    description="Displays information about Chatty Bot."
)
async def about_command(interaction: discord.Interaction):
    catchphrase = "Talk owl day, hooole day."
    description = (
        f"🦉 **Chatty Bot** — {catchphrase}\n"
        f"Version: {RELEASED_VERSION}\n"
        "A versatile, friendly Discord utility bot providing fun and useful commands for your community.\n"
        "Updated: July 19, 2025 (UTC)"
    )
    await interaction.response.send_message(description, ephemeral=True)

# ----- scmd#1 / dice [sides]
# --- constant ---
number_emojis = {
    0: "0⃣", 
    1: "1⃣", 
    2: "2⃣", 
    3: "3⃣", 
    4: "4⃣", 
    5: "5⃣",
    6: "6⃣", 
    7: "7⃣", 
    8: "8⃣", 
    9: "9⃣", 
    10: "🔟"
}
# --- @ ---
@tree.command(
    name="dice",
    description="Roll the dice. Optionally, you can specify the number of sides."
)
@app_commands.describe(
    sides="number of sides of the dice [Integer greater than 0 | default: 6]"
 )
async def dice(interaction: discord.Interaction, sides: int = 6):
    if sides < 1:
        await interaction.response.send_message("🤔", ephemeral=True)
        return

    await interaction.response.defer()
    await interaction.followup.send(f"I rolled the {sides} face dice 🎲 and got...")

    result = random.randint(1, sides)
    
    if result <= 10:
        result_emoji = number_emojis.get(result, str(result))
    else:
        result_emoji = "".join(number_emojis.get(int(d), d) for d in str(result))
    
    await interaction.followup.send(result_emoji)


# ----- scmd#2 / timezones
# --- @ ---
@tree.command(
    name="ntime", 
    description="Displays the current time. Optionally, you can specify the time zone."
)
@app_commands.describe(
    tz="timezone [00 or 00:00 | default: 0]"
 )
async def timezones_command(interaction: discord.Interaction, tz: str = None):
    # default
    target_tz = timezone.utc

    # regular expression support for offset specification (e.g., "9", "+9", "-5", "09:00", "-05:30")
    offset = 0
    if tz:
        match = re.match(r'^([+-]?)(\d{1,2})(?::?(\d{2}))?$', tz.strip())
        if match:
            sign = -1 if match.group(1) == '-' else 1
            hours = int(match.group(2))
            minutes = int(match.group(3) or 0)
            offset = sign * (hours + minutes / 60)
            target_tz = timezone(timedelta(hours=offset))
        else:
            return await interaction.response.send_message("Invalid timezone format. Use +09, -5, 09:30 etc.")

    now = datetime.now(target_tz)
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    response = f"Current time (UTC{offset:+}) : {now.strftime(fmt)}"
    await interaction.response.send_message(response)

# ----- scmd#3 / dailytasks

WEEKLY_TASKS = {
    'Monday': [
        "Catch any OCG and Interrogate Them in RP Process",
        "Complete 2 Training Sessions",
        "Conduct 2 Interviews",
        "Conduct Recruitment in APD"
    ],
    'Tuesday': [
        "Do Any Event with Your Members",
        "Patrol YPD and Check",
        "Conduct 1 Interview"
    ],
    'Wednesday': [
        "Conduct Recruitment in MU",
        "Conduct 2 Trainings",
        "Participate in Main House",
        "Conduct 1 Lecture"
    ],
    'Thursday': [
        "Conduct 2 Lectures",
        "Conduct 2 Training Sessions",
        "Conduct 2 Interviews"
    ],
    'Friday': [
        "Arrest 2 Criminals",
        "Conduct 1 Training Session",
        "Conduct 1 Interview",
        "Conduct 1 Lecture"
    ],
# 'Saturday': [
#     "Patrol the City of Yuzhny for 30 minutes",
#     "Conduct 2 Lectures",
#     "Conduct 2 Training Sessions"
# ],
    'Saturday': [],
    'Sunday': []
}

def create_daily_message(date, weekday, tasks):
    def format_date(dt):
        day = dt.day
        month = calendar.month_name[dt.month]
        year = dt.year
        return f"{day} {month} {year}"

    if not tasks:
        task_str = "*NO TASK today as it is holidays*"
    else:
        task_str = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])

    message = (
        ":detective: Greetings SIS Director, \n"
        f"# :clipboard:  Today's Missions\n"
        f"-# {format_date(date)}\n"
        f"{task_str}\n"
        "**Have a good day! :muscle: :sparkles: **\n"
        "-# Just a reminder to submit the Curator Task Report by 23:59 server time today. You can pass on some of the tasks to Deputies or other Senior Staff if needed."
    )
    return message

async def send_daily_task_message(channel):

    now = datetime.now(MSK)
    weekday = calendar.day_name[now.weekday()]
    tasks = WEEKLY_TASKS.get(weekday, [])

    await channel.send(create_daily_message(now, weekday, tasks))
    await channel.send("<@1369794386132471858>")

async def scheduled_send():
    channel = bot.get_channel(1395289929126252586)
    if channel:
        await send_daily_task_message(channel)
    
 # --- @ ---
@tree.command(
    name="dailytasks", 
    description="Displays today's SIS tasks (MSK / UTC+3)",
    guilds=ADMIN_GUILD
)
async def dailytask_command(interaction: discord.Interaction):
    now = datetime.now(MSK)
    weekday = calendar.day_name[now.weekday()]
    tasks = WEEKLY_TASKS.get(weekday, [])

    await interaction.response.send_message(create_daily_message(now, weekday, tasks))

# -------------- prefix-commands -------------- 
# ----- pcmd#1 /adminlist
# --- @ ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('/adminlist') or (
        message.attachments and message.attachments[0].filename.endswith('.txt')
    ):
        if message.attachments:
            attachment = message.attachments[0]
            data = await attachment.read()
            text = data.decode('utf-8')
        else:
            text = message.content

        lines = text.strip().split('\n')

        if len(lines) <= 1:
            await message.channel.send("⚠️ Insufficient data.")
            return

        data_lines = lines[1:]
        admins = []

        for i in range(0, len(data_lines), 5):
            if i + 4 >= len(data_lines):
                break

            name = data_lines[i + 1].strip()
            rank = data_lines[i + 2].strip()

            if name and rank.isdigit():
                admins.append((int(rank), name))

        if not admins:
            await message.channel.send("⚠️ No valid admin data.")
            return

        admins.sort(reverse=True)
        date_str = datetime.now().strftime('%Y/%m/%d')

        admin_rank = len(admins)
        header = f"# Admins List - {admin_rank}\n-# {date_str}\n"
        entries = []
        for idx, (count, name) in enumerate(admins, start=1):
            if count >= 6:
                emoji = "👑"
            elif count == 5:
                emoji = "🎩"
            else:
                emoji = ""
            
            line = f"{idx}. {emoji} ({count}) {name}" if emoji else f"{idx}. ({count}) {name}"
            entries.append(line)

        batch = header
        for line in entries:
            if len(batch) + len(line) + 1 > 1900:
                await message.channel.send(batch)
                await asyncio.sleep(1.0)
                batch = ""
            batch += line + "\n"

        if batch.strip():
            await message.channel.send(batch)

# -------------- on_ready -------------- 
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

    target_guild_ids = list(set(ALL_GUILD_IDS + ADMIN_GUILD_IDS))

    for guild_id in target_guild_ids:
        try:
            synced = await bot.tree.sync(guild=discord.Object(id=guild_id))
            print(f"SYNCED: Synced {len(synced)} commands to guild {guild_id}")
        except Exception as e:
            print(f"FAILED: Failed to sync commands for guild {guild_id}: {e}")
            
    # --- Set bot presence/status ---
    description = "Chatty Bot"
    activity = discord.Game(name=f"v{RELEASED_VERSION} • {description}")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
    
    if not hasattr(bot, 'scheduler_started'):
        scheduler = AsyncIOScheduler(timezone=MSK)
        async def job():
            channel = bot.get_channel(1395289929126252586)
            if channel:
                await send_daily_task_message(channel)
        scheduler.add_job(job, 'cron', hour=6, minute=0)
        scheduler.start()
        bot.scheduler_started = True


# -------------- Render -------------- 
# --- keep alive ---
keep_alive()

# --- TOKEN ---
TOKEN = os.getenv("DISCORD_TOKEN")  # from environment variables in Render
print(f"TOKEN is None: {TOKEN is None}") 

# -------------- RUN BOT -------------- 
bot.run(TOKEN)