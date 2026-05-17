import discord
from commands.utils import cargar_autoroles, guardar_autoroles


def setup_bmy_commands(bmy):
    @bmy.command(name="setautorol", description="Configura el rol que se asignará automáticamente.")
    async def setautorol(interaction, rol: discord.Role):
        autoroles = cargar_autoroles()
        autoroles[str(interaction.guild.id)] = rol.id
        guardar_autoroles(autoroles)
        await interaction.response.send_message(f"Rol configurado: {rol.name}")

    @bmy.command(name="avatar", description="Muestra el avatar de un usuario por mención o ID.")
    async def avatar(interaction, usuario: str):

        #Obtener usuario por mencion
        if usuario.startswith("<@") and usuario.endswith(">"):
            usuario = usuario.replace("<@", "").replace(">", "").replace("!", "")

        #Intentar obtenerlo del server
        member = interaction.guild.get_member(int(usuario)) if usuario.isdigit() else None

        #Si no esta buscarlo globalmente
        if member is None:
            try:
                member = await interaction.client.fetch_user(int(usuario))
            except:
                await interaction.response.send_message("❌ No pude encontrar ese usuario.")
                return
        
        #Obtener avatar
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

        await interaction.response.send_message(avatar_url)

    @bmy.command(name="banner", description="Muestra el banner de un usuario por mención o ID.")
    async def banner(interaction, usuario: str):

        # Si es mención tipo <@123> o <@!123>
        if usuario.startswith("<@") and usuario.endswith(">"):
            usuario = usuario.replace("<@", "").replace(">", "").replace("!", "")

        # Intentar obtenerlo del servidor
        member = interaction.guild.get_member(int(usuario)) if usuario.isdigit() else None

        # Si no está en el servidor, buscarlo globalmente
        if member is None:
            try:
                member = await interaction.client.fetch_user(int(usuario))
            except:
                await interaction.response.send_message("❌ No pude encontrar ese usuario.")
                return

        # Verificar si tiene banner
        if member.banner is None:
            await interaction.response.send_message("⚠️ Ese usuario no tiene banner.")
            return

        # Obtener banner
        banner_url = member.banner.url

        await interaction.response.send_message(banner_url)
    
    @bmy.command(name="info", description="Escanea a un usuario como si fueras Lucy.")
    async def info(interaction, usuario: str):

        # Si es mención tipo <@123> o <@!123>
        if usuario.startswith("<@") and usuario.endswith(">"):
            usuario = usuario.replace("<@", "").replace(">", "").replace("!", "")

        # Intentar obtenerlo del servidor
        member = interaction.guild.get_member(int(usuario)) if usuario.isdigit() else None

        # Si no está en el servidor, buscarlo globalmente
        if member is None:
            try:
                member = await interaction.client.fetch_user(int(usuario))
            except:
                await interaction.response.send_message("❌ [ERROR] No se pudo establecer conexión con el objetivo.")
                return

        # Crear embed estilo Lucy
        embed = discord.Embed(
            title=f"⟦ SCAN INICIADO ⟧",
            description=f"Accediendo a los datos del objetivo...\n> **{member.name}**",
            color=discord.Color.from_rgb(0, 170, 255)  # Azul eléctrico Lucy
        )

        # Avatar
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed.set_thumbnail(url=avatar_url)

        # Banner (si tiene)
        if member.banner:
            embed.set_image(url=member.banner.url)

        # ID
        embed.add_field(
            name="🧬 Identificación",
            value=f"`{member.id}`",
            inline=False
        )

        # Fecha de creación
        embed.add_field(
            name="📅 Registro del sistema",
            value=f"`{member.created_at.strftime('%d/%m/%Y %H:%M')}`",
            inline=False
        )

        # Si está en el servidor, agregar roles y fecha de unión
        if isinstance(member, discord.Member):

            embed.add_field(
                name="📥 Integración al servidor",
                value=f"`{member.joined_at.strftime('%d/%m/%Y %H:%M')}`",
                inline=False
            )

            # Roles
            roles = [role.mention for role in member.roles if role.name != "@everyone"]
            roles_text = ", ".join(roles) if roles else "`Sin roles asignados`"

            embed.add_field(
                name="🎭 Permisos / Roles",
                value=roles_text,
                inline=False
            )

        # Footer estilo Lucy
        embed.set_footer(text="⟦ Netrunner: Lucy ⟧  •  Acceso concedido")

        await interaction.response.send_message(embed=embed)


