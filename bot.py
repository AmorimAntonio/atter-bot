import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # pegando o token do .env

keep_alive()  # manter o bot ativo

# definindo as permissões do bot
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

# definindo o prefixo do bot, nesse caso "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs das mensagens (substitua após rodar !setup)
LEVEL_ROLE_MESSAGE_ID = 1421134569918173284  # mensagem de função
AREA_ROLE_MESSAGE_ID = 1421134587752480811   # mensagem de área

# mapeando emojis para os cargos correspondentes

# função:
LEVEL_EMOJI_ROLE_MAP = {
    "🎓": 1379831905251233804,  # Senior
    "🛠️": 1379790093304332348,  # Pleno
    "⚙️": 1379832214099067101,  # Junior
    "☕": 1379790221968806098,  # Estagiário(a)
    "🌱": 1379790296518365226,  # Trainee
}

# área de atuação:
AREA_EMOJI_ROLE_MAP = {
    "🎲": 1379832013682380810,  # Engenharia de dados
    "📊": 1379790435592966287,  # Analista de dados
    "🧪": 1379790497345962146,  # Cientista de dados
}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")  # printando no log quando o bot fica online 

@bot.command()
async def setup(ctx):  # quando o usuário digita "!setup"
    # mensagem 1: função
    level_msg = await ctx.send(
        "Reaja para indicar seu nível de experiência:\n\n"
        "🎓 - Sênior\n"
        "🛠️ - Pleno\n"
        "⚙️ - Júnior\n"
        "☕ - Estagiário(a)\n"
        "🌱 - Trainee"
    )
    for emoji in LEVEL_EMOJI_ROLE_MAP.keys():
        await level_msg.add_reaction(emoji)
    print(f"ID da mensagem de função: {level_msg.id}")

    # mensagem 2: área de atuação
    area_msg = await ctx.send(
        "Reaja para receber um cargo:\n\n"
        "🎲 - Engenharia de dados\n"
        "📊 - Analista de dados\n"
        "🧪 - Cientista de dados"
    )
    for emoji in AREA_EMOJI_ROLE_MAP.keys():
        await area_msg.add_reaction(emoji)
    print(f"ID da mensagem de área: {area_msg.id}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    # detectando qual mensagem foi reagida
    if payload.message_id == LEVEL_ROLE_MESSAGE_ID:
        role_id = LEVEL_EMOJI_ROLE_MAP.get(str(payload.emoji))
    elif payload.message_id == AREA_ROLE_MESSAGE_ID:
        role_id = AREA_EMOJI_ROLE_MAP.get(str(payload.emoji))
    else:
        return

    if not role_id:
        return

    # pegando o cargo correspondente
    member = guild.get_member(payload.user_id)
    if member:
        role = guild.get_role(role_id)
        if role:
            await member.add_roles(role)
            print(f"Adicionado {role.name} para {member.display_name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    # detectando qual mensagem teve a reação removida
    if payload.message_id == LEVEL_ROLE_MESSAGE_ID:
        role_id = LEVEL_EMOJI_ROLE_MAP.get(str(payload.emoji))
    elif payload.message_id == AREA_ROLE_MESSAGE_ID:
        role_id = AREA_EMOJI_ROLE_MAP.get(str(payload.emoji))
    else:
        return

    if not role_id:
        return

    member = guild.get_member(payload.user_id)
    if member:
        role = guild.get_role(role_id)
        if role:
            await member.remove_roles(role)
            print(f"Removido {role.name} de {member.display_name}")

bot.run(TOKEN)