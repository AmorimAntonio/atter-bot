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

def salvar_ids(level_id, area_id):
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "level_message_id": level_id,
            "area_message_id": area_id
        }, f)


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
    str("🎓"): 1379831905251233804,
    str("🛠️"): 1379790093304332348,
    str("⚙️"): 1379832214099067101,
    str("☕"): 1379790221968806098,
    str("🌱"): 1379790296518365226,
}


# área de atuação:
AREA_EMOJI_ROLE_MAP = {
    str("🎲"): 1379832013682380810,  # Engenharia de dados
    str("📊"): 1379790435592966287,  # Analista de dados
    str("🧪"): 1379790497345962146,  # Cientista de dados
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
    salvar_ids(level_msg.id, area_msg.id)

    print(f"IDs salvos: função={level_msg.id}, área={area_msg.id}")


@bot.event
async def on_raw_reaction_add(payload):
    print("🟡 Evento de reação detectado")
    print(f"Mensagem: {payload.message_id} | Emoji: {payload.emoji}")
    print(f"emoji.name: {payload.emoji.name}, str: {str(payload.emoji)}, id: {getattr(payload.emoji, 'id', None)}")
    print(f"emoji.name: {payload.emoji.name}")
    print(f"emoji str : {str(payload.emoji)}")


    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    level_id, area_id = carregar_ids()

    if payload.message_id == level_id:
        role_id = LEVEL_EMOJI_ROLE_MAP.get(payload.emoji.name)
    elif payload.message_id == area_id:
        role_id = AREA_EMOJI_ROLE_MAP.get(payload.emoji.name)
    else:
        return

    if not role_id:
        print("⚠️ Emoji não mapeado para cargo.")
        return

    try:
        member = await guild.fetch_member(payload.user_id)
        role = guild.get_role(role_id)

        if member and role:
            print(f"Tentando atribuir cargo: {role.name} para {member.display_name}")
            await member.add_roles(role)
            print(f"✅ Cargo {role.name} atribuído a {member.display_name}")
        else:
            print("⚠️ Membro ou cargo não encontrado.")
    except Exception as e:
        print(f"❌ Erro ao adicionar cargo: {e}")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    # detectando qual mensagem teve a reação removida
    level_id, area_id = carregar_ids()
    if payload.message_id == level_id:
        role_id = LEVEL_EMOJI_ROLE_MAP.get(payload.emoji.name)
    elif payload.message_id == area_id:
        role_id = AREA_EMOJI_ROLE_MAP.get(payload.emoji.name)
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