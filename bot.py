import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="How do I verify?",
        style=discord.ButtonStyle.secondary,
        custom_id="verify_info_btn"
    )
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Go to the verification channel and fill out the form!",
            ephemeral=True
        )

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    bot.add_view(VerificationView())
    try:
        # Syncs slash commands globally with Discord
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# 1. /send_verify_notice Slash Command
@bot.tree.command(name="send_verify_notice", description="Sends the verification notice with button")
@app_commands.checks.has_permissions(administrator=True)
async def send_verify_notice(interaction: discord.Interaction):
    embed = discord.Embed(
        description="You can't view this channel, you are not verified.",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed, view=VerificationView())

# 2. /say Slash Command
@bot.tree.command(name="say", description="Makes the bot send a message in the channel")
@app_commands.checks.has_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Message sent!", ephemeral=True)
    await interaction.channel.send(message)

bot.run(os.getenv("BOT_TOKEN"))
