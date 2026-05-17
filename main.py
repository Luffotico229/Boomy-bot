import os 
import discord
from discord import Intents, app_commands
from dotenv import load_dotenv 
import json

def cargar_autoroles():
    try:
        with open('autoroles.json', 'r') as f:
            return json.load(f)
    except:
        return {}
    
def guardar_autoroles(data):
    with open("autoroles.json", "w") as f:
        json.dump(data, f, indent=4)

# Cargar token desde .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Activar Intents
intents = Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot conectado como {client.user}")

@tree.command(name="setautorol", description="Configura el rol que se asignará automáticamente.")
async def setautorol(interaction, rol: discord.Role):
    autoroles = cargar_autoroles()
    autoroles[str(interaction.guild.id)] = rol.id
    guardar_autoroles(autoroles)
    await interaction.response.send_message(f"Rol configurado: {rol.name}")

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







