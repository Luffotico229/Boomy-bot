import os 
import discord
from discord import Intents
from dotenv import load_dotenv 

# Cargar token desde .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Nombre EXACTO del rol q quieres asignar
TARGET_ROLE_NAME = "𝐜𝐨𝐦𝐮𝐧𝐢𝐝𝐚𝐝"

# Activar Intents
intents = Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_member_join(member):
    print(f"Nuevo miembro: {member}")

    guild = member.guild
    role = discord.utils.get(guild.roles, name=TARGET_ROLE_NAME)

    if role is None:
        print(f'⚠️   Rol "{TARGET_ROLE_NAME}" no encontrado en el servidor.')
        return 

    # Verificar jerarquia de roles
    bot_member = guild.get_member(client.user.id)
    if role >= bot_member.top_roles:
        print(f"⚠️  El rol '{TARGET_ROLE_NAME}' está por encima der rol del bot. Súbelo en la jerarquía.") 
        return 

    try:
        await member.add_roles(role, reason="Autorol automático")
        print(f"✔️  Rol '{TARGET_ROLE_NAME}' asignado a {member}")
    except Exception as e:
        print(f"❌ Error asignando rol: {e}")

client.run(TOKEN)







