import os 
import discord
from discord import Intents, app_commands
from dotenv import load_dotenv 
from commands.bmy_commands import setup_bmy_commands
from commands.utils import cargar_autoroles

# Cargar token desde .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Activar Intents
intents = Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bmy = app_commands.Group(name="bmy", description="Comandos de Boomy")
tree.add_command(bmy)
setup_bmy_commands(bmy)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot conectado como {client.user}")

@client.event
async def on_member_join(member):
    autoroles = cargar_autoroles()

    guild_id = str(member.guild.id)

    if guild_id not in autoroles:
        print("⚠️ No hay autorol configurado para este servidor.") 
        return 

    rol_id = autoroles[guild_id]
    role = member.guild.get_role(rol_id)

    if role is None:
        print(f'⚠️  El rol guardado ya no existe en el servidor.')
        return 

    # Verificar jerarquia de roles
    bot_member = member.guild.get_member(client.user.id)
    if role >= bot_member.top_role:
        print(f"⚠️ El rol esta por encima del bot.") 
        return 

    try:
        await member.add_roles(role, reason="Autorol automático")
        print(f"✔️ Rol '{role.name}' asignado a {member}")
    except Exception as e:
        print(f"❌ Error asignando rol: {e}")

client.run(TOKEN)







