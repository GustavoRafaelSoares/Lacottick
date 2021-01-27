from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import has_permissions
from discord.ext.commands import CheckFailure

from ..db import db

class Adm(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='prefix')
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            await ctx.send("O prefixo não pode ser maior que 5 letras")
        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            await ctx.send(f"Prefixo alterado para {new}.")

    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send('Voce precisa ter permissões de administrador para fazer estas alterações')

#banir, desbanir, kickar usuarios
#remover inativos


    @Cog.listener()
    async def on_member_join(self, member):
        db.execute('INSERT INTO exp (UserID) VALUES (?)', member.id)
        await self.bot.get_channel(782589531035140096).send(f'Bem Vindo a **{member.guild.name}** {member.mention}! Va para <#784454139040104468> para conversar!')
        try:
            await member.send(f'Bem vindo a **{member.guild.name}**! aproveite os servidor!')
        except Forbidden:
            pass

        await member.add_roles(member.guild.get_role(803981773133971456))
    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute('DELETE FROM exp WHERE UserID = ?', member.id)
        await self.bot.get_channel(782589531035140096).send(f'O usuario {member.display_name} saiu do servidor.')



    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('adm')

def setup(bot):
    bot.add_cog(Adm(bot))
