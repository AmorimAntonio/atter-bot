import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # pegando o token do .env

CONFIG_FILE = "config.json"

# função para pegar os IDs do json
def carregar_ids():
    try:
        with open(CONFIG_FILE, "r") as f:
            dados = json.load(f)
            return dados.get("level_message_id"), dados.get("area_message_id")
    except FileNotFoundError:
        return None, None


# definindo as permissões do bot
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

# definindo o prefixo do bot, nesse caso "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs das mensagens (funcionando de forma dinâmica)
LEVEL_ROLE_MESSAGE_ID, AREA_ROLE_MESSAGE_ID = carregar_ids()

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
async def setup(ctx):
    # Envia mensagens
    level_msg = await ctx.send("Reaja para indicar seu nível de experiência:\n\n..."
                               "🎓 - Sênior\n🛠️ - Pleno\n⚙️ - Júnior\n☕ - Estagiário(a)\n🌱 - Trainee")
    for emoji in LEVEL_EMOJI_ROLE_MAP:
        await level_msg.add_reaction(emoji)

    area_msg = await ctx.send("Reaja para sua área de atuação:\n\n..."
                              "🎲 - Engenharia de dados\n📊 - Analista de dados\n🧪 - Cientista de dados")
    for emoji in AREA_EMOJI_ROLE_MAP:
        await area_msg.add_reaction(emoji)

    # Salva os IDs dinamicamente
    carregar_ids(level_msg.id, area_msg.id)

    print(f"IDs salvos: função={level_msg.id}, área={area_msg.id}")


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

def carregar_ids():
    with open(CONFIG_FILE, "r") as f:
        dados = json.load(f)
        return dados.get("level_message_id"), dados.get("area_message_id")



bot.run(TOKEN)