import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Mapeamentos de emojis para IDs de cargos
POSITION_ROLE_MAP = {
    "🎲": 1365322123458908170,  # Engenheiro de dados
    "📊": 1379472452861689916,  # Analista de dados
    "🧪": 1379099857834213506   # Cientista de dados (coloque o ID real)
}

LEVEL_ROLE_MAP = {
    "🎓": 1379472505055608902,  # Sênior
    "🛠️": 1379472556993548319,  # Pleno
    "⚙️": 1379472533346324541,  # Júnior
    "☕": 1379099812758163537,  # Estagiário
    "🌱": 1379472577663078582   # Trainee
}

# Armazenar os IDs das mensagens após o setup
POSITION_MESSAGE_ID = None
LEVEL_MESSAGE_ID = None

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def setup(ctx):
    global POSITION_MESSAGE_ID, LEVEL_MESSAGE_ID

    # Mensagem 1: Cargos da empresa
    msg1 = await ctx.send("Reaja para receber um cargo da empresa:\n🎲 - Engenheiro de Dados\n📊 - Analista de Dados\n🧪 - Cientista de Dados")
    for emoji in POSITION_ROLE_MAP.keys():
        await msg1.add_reaction(emoji)
    POSITION_MESSAGE_ID = msg1.id
    print(f"ID da mensagem de cargos: {POSITION_MESSAGE_ID}")

    # Mensagem 2: Faixa de experiência
    msg2 = await ctx.send("Reaja para indicar seu nível de experiência:\n🎓 - Sênior\n🛠️ - Pleno\n⚙️ - Júnior\n☕ - Estagiário\n🌱 - Trainee")
    for emoji in LEVEL_ROLE_MAP.keys():
        await msg2.add_reaction(emoji)
    LEVEL_MESSAGE_ID = msg2.id
    print(f"ID da mensagem de níveis: {LEVEL_MESSAGE_ID}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    member = guild.get_member(payload.user_id)
    if not member:
        return

    # Verifica se a reação foi em uma das mensagens esperadas
    if payload.message_id == POSITION_MESSAGE_ID:
        role_id = POSITION_ROLE_MAP.get(str(payload.emoji))
    elif payload.message_id == LEVEL_MESSAGE_ID:
        role_id = LEVEL_ROLE_MAP.get(str(payload.emoji))
    else:
        return

    if role_id:
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

    member = guild.get_member(payload.user_id)
    if not member:
        return

    if payload.message_id == POSITION_MESSAGE_ID:
        role_id = POSITION_ROLE_MAP.get(str(payload.emoji))
    elif payload.message_id == LEVEL_MESSAGE_ID:
        role_id = LEVEL_ROLE_MAP.get(str(payload.emoji))
    else:
        return

    if role_id:
        role = guild.get_role(role_id)
        if role:
            await member.remove_roles(role)
            print(f"Removido {role.name} de {member.display_name}")

bot.run(TOKEN)
