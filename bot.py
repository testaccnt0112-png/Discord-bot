import os
import discord
from discord.ext import commands

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

@bot.command()
@commands.has_permissions(administrator=True)
async def send_verify_notice(ctx):
    embed = discord.Embed(
        description="You can't view this channel, you are not verified.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed, view=VerificationView())

bot.run(os.getenv("MTUzNTMzOTYxMTA5MjY4NDg2MQ.GXiv2M.j_o5C4sz0fXmD0PAu1hHytQfDGElCcJ1mr1gMI"))
