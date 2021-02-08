from typing import Optional
from datetime import datetime

from discord.ext.commands import Cog, Greedy
from discord.ext.commands import command, Member
from discord.ext.commands import has_permissions
from discord.ext.commands import CheckFailure, bot_has_permissions

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

    @command(name='kick')
    @bot_has_permissions(Kick_members=True)
    @has_permissions(Kick_members=True)
    async def Kick_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'Sem motivo aparente'):
        if not len(targets):
            await ctx.send('Um ou mais argumentos são requeridos para esta ação')

        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissons.administrator:
                    await target.kick(reason=reason)

                    embed = Embed(title='Membro Kicado',
                                  colour=0xDD2222,
                                  timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=target.avatar_url)
                    fields = [('Membro', f'{target.name} vulgo {member.display_name}', False),
                             ('Banido por', ctx.author.display_name, False),
                             ('Motivo', reason, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.log_channel.send(embed=embed)
                else:
                    await ctx.send('f{target.display_name} não pode ser kicado')
            await ctx.send('Ação concluida')


    @Kick_members.error
    async def Kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send('Permissões insuficientes para esta ação')

    @command(name='banir')
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def Ban_members(self, ctx, targets: Greedy[Member], *, reason: Optional[str] = 'Sem motivo aparente'):
        if not len(targets):
            await ctx.send('Um ou mais argumentos são requeridos para esta ação')

        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position and not target.guild_permissons.administrator:
                    await target.ban(reason=reason)

                    embed = Embed(title='Membro Banido',
                                  colour=0xDD2222,
                                  timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=target.avatar_url)
                    fields = [('Membro', f'{target.name} vulgo {member.display_name}', False),
                             ('Banido por', ctx.author.display_name, False),
                             ('Motivo', reason, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    await self.log_channel.send(embed=embed)
                else:
                    await ctx.send(f'{target.display_name} não pode ser banido')
            await ctx.send('Ação concluida')

    @Ban_members.error
    async def Ban_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send('Permissões insuficientes para esta ação')

#punições
#ban temporario em alguma sala, com restrições

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('adm')
            self.log_channel = self.bot.get_channel(782589531035140096)

def setup(bot):
    bot.add_cog(Adm(bot))
