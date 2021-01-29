from datetime import datetime

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from discord import Forbidden

from ..db import db

class Logs(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('logs')
            self.log_channel = self.bot.get_channel(782589531035140096)

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute('INSERT INTO exp (UserID) VALUES (?)', member.id)
        await self.log_channel.send(f'Bem Vindo a **{member.guild.name}** {member.mention}! Va para <#784454139040104468> para conversar!')
        try:
            await member.send(f'Bem vindo a **{member.guild.name}**! aproveite os servidor!')
        except Forbidden:
            pass

        await member.add_roles(member.guild.get_role(803981773133971456))
    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute('DELETE FROM exp WHERE UserID = ?', member.id)
        await self.log_channel.send(f'O usuario {member.display_name} saiu do servidor.')

    @cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            embed = Embed(title='Atualização de usuario',
                          description='Alteração de Nome',
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            fields = [("Antigo", before.name, False),
                      ("Novo", after.name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.discriminator != after.discriminator:
            embed = Embed(title='Atualização de usuario',
                          description='Alteração de descriminante',
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            fields = [("Antigo", before.discriminator, False),
                      ("Novo", after.discriminator, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)

        if before.avatar_url != after.avatar_url:
             embed = Embed(title='Atualização de usuario',
                           description='Alteração de Imagem de Perfil (A imagem abaixo é a nova!)',
                           colour=self.log_channel.guild.get_member(after.id).colour,
                           timestamp=datetime.utcnow())

             embed.set_thumbnail(url=before.avatar_url)
             embed.set_image(url=after.avatar_url)

             await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title='Atualização de usuario',
                          description='Alteração de apelido',
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            fields = [("Antigo", before.display_name, False),
                      ("Novo", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

            await self.log_channel.send(embed=embed)


    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            pass

    @Cog.listener()
    async def on_message_delete(self, before, after):
        if not after.author.bot:
            pass




def setup(bot):
    bot.add_cog(Logs(bot))
