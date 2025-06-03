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

ROLE_MESSAGE_ID = 1379108215450632347  # ID da mensagem que com as reações

# mapeando emojis para os cargos correspondentes
EMOJI_ROLE_MAP = {
    # função:
    "🎓": 1379472505055608902,  # Senior
    "🛠️": 1379472556993548319,  # Pleno
    "⚙️": 1379472533346324541,  # Junior
    "☕": 1379099812758163537,  # Estágiário(a)
    "🌱": 1379472577663078582,  # Trainee

    # faixa de experiência:
    "🎲": 1365322123458908170,  # Engenharia de dados
    "📊": 1379472452861689916,  # Analista de dados
    "🧪": 1379099857834213506,  # Cientista de dados
}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")  # printando no log quando o bot fica online 

@bot.command()
async def setup(ctx):  # quando o usuário digita "!setup"
    # mensagem:
    msg = await ctx.send(
        "Reaja para receber um cargo:\n\n"
        "**Função:**\n"
        "🎓 - Senior\n"
        "🛠️ - Pleno\n"
        "⚙️ - Junior\n"
        "☕ - Estagiário(a)\n"
        "🌱 - Trainee\n\n"
        "**Área de Atuação:**\n"
        "🎲 - Engenharia de dados\n"
        "📊 - Analista de dados\n"
        "🧪 - Cientista de dados"
    )
    # emotes:
    for emoji in EMOJI_ROLE_MAP.keys():
        await msg.add_reaction(emoji)
    # printando o id da mensagem enviada
    print(f"ID da mensagem: {msg.id}")

@bot.event
async def on_raw_reaction_add(payload):
    # verificando quando alguém reage à mensagem
    if payload.message_id != ROLE_MESSAGE_ID or payload.user_id == bot.user.id:
        return
    # ignorando as reações do próprio bot
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    role_id = EMOJI_ROLE_MAP.get(str(payload.emoji))
    if not role_id:
        return

    # pegando o cargo correspondente ao emote
    member = guild.get_member(payload.user_id)
    if member:
        role = guild.get_role(role_id)
        if role:
            await member.add_roles(role)  # buscando o membro e adicionando o cargo
            print(f"Adicionado {role.name} para {member.display_name}")

@bot.event
async def on_raw_reaction_remove(payload):  # assim como o anterior
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
