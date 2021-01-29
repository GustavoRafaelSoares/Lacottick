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
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('adm')

def setup(bot):
    bot.add_cog(Adm(bot))
