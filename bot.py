import os
import discord
from discord import app_commands
from discord.ext import commands


# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Bot ID: {bot.user.id}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")

        for command in synced:
            print(f"  /{command.name}")

    except Exception as e:
        print(f"Failed to sync commands: {e}")


# =========================
# /say
# =========================

@bot.tree.command(
    name="say",
    description="Make the bot send a message"
)
@app_commands.describe(
    message="The message you want the bot to send"
)
async def say(
    interaction: discord.Interaction,
    message: str
):
    await interaction.response.send_message(message)


# =========================
# /embed
# =========================

@bot.tree.command(
    name="embed",
    description="Send an embed message"
)
@app_commands.describe(
    title="Embed title",
    description="Embed description"
)
async def embed(
    interaction: discord.Interaction,
    title: str,
    description: str
):

    embed_message = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blurple()
    )

    embed_message.set_footer(
        text=f"Sent by {interaction.user}"
    )

    await interaction.response.send_message(
        embed=embed_message
    )


# =========================
# BUTTON
# =========================

class MyButton(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Click Me",
        style=discord.ButtonStyle.primary,
        custom_id="my_button"
    )
    async def button_callback(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "You clicked the button! 👋"
        )


# =========================
# /button
# =========================

@bot.tree.command(
    name="button",
    description="Send a message with a button"
)
async def button(
    interaction: discord.Interaction
):

    view = MyButton()

    await interaction.response.send_message(
        "Click the button below!",
        view=view
    )


# =========================
# START BOT
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN environment variable is missing."
    )

bot.run(TOKEN)
