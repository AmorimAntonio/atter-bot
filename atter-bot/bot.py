import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True


bot = commands.Bot(command_prefix="!", intents=intents)

# ID da mensagem que terá as reações
ROLE_MESSAGE_ID = 1379107027481002057  # substitua pelo ID real da mensagem
EMOJI_ROLE_MAP = {
    "🎲": 1379099857834213506,  # ID do cargo Fogo
    "☕": 1379099812758163537,  # ID do cargo Gelo
}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def setup(ctx):
    msg = await ctx.send("Reaja para receber um cargo: 🎲 - Cientista de dados, ☕ - Estágiario")
    await msg.add_reaction("🎲")
    await msg.add_reaction("☕")
    print(f"ID da mensagem: {msg.id}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != ROLE_MESSAGE_ID or payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    role_id = EMOJI_ROLE_MAP.get(str(payload.emoji))
    if not role_id:
        return

    member = guild.get_member(payload.user_id)
    if member:
        role = guild.get_role(role_id)
        if role:
            await member.add_roles(role)
            print(f"Adicionado {role.name} para {member.display_name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != ROLE_MESSAGE_ID or payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    role_id = EMOJI_ROLE_MAP.get(str(payload.emoji))
    if not role_id:
        return

    member = guild.get_member(payload.user_id)
    if member:
        role = guild.get_role(role_id)
        if role:
            await member.remove_roles(role)
            print(f"Removido {role.name} de {member.display_name}")

bot.run(TOKEN)