from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

class Inf(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command(name='userinfo', aliases=['ui'])
    async def user_info(self, ctx, target: Optional[Member]):

        target = target or ctx.author

        embed = Embed(title='Informações do Usuario',
                      colour=target.colour,
                      timestamp=datetime.utcnow())

        fields=[('ID', target.id, False),
                ('Nome', str(target), True),
                ('Bot?', target.bot, True),
                ('Maior Cargo', target.top_role.mention, True),
                ('Status', str(target.status).title() if target.status else 'Offline', True),
                ('Atividade', f'{str(target.activity.type).split(".")[-1].title() if target.activity else "N/A"} {target.activity.name if target.activity else "" }', True),
                ('Criado em', target.created_at.strftime('%d/%m/%y %H:%M:%S'), True),
                ('Entrou em', target.joined_at.strftime('%d/%m/%y %H:%M:%S'), True),
                ('Nitro', bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=target.avatar_url)

        await ctx.send(embed=embed)

    @command(name='serverinfo', aliases=['si'])
    async def server_info(self, ctx):
        embed = Embed(title='Informações do Servidor',
                      colour=ctx.guild.owner.colour,
                      timestamp=datetime.utcnow())

        statuses = [len(list(filter(lambda m: str(m.status) == 'online', ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == 'idle', ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == 'dnd', ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == 'offline', ctx.guild.members))),]

        fields=[('ID', ctx.guild.id, True),
                ('Dono', ctx.guild.owner, True),
                ('Região', ctx.guild.region, True),
                ('Criado em', ctx.guild.created_at.strftime('%d/%m/%y %H:%M:%S'), True),
                ('Membros', len(ctx.guild.members), True),
                ('Humanos', len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                ('Bots', len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                ('Membros Banidos', len(await ctx.guild.bans()), True),
                ('Status dos Usuarios', f':green_circle:{statuses[0]} :yellow_circle:{statuses[1]} :red_circle:{statuses[2]} :white_circle:{statuses[3]}', True),
                ("Canais de Texto", len(ctx.guild.text_channels), True),
                ('Canais de Voz', len(ctx.guild.voice_channels), True),
                ('Categorias', len(ctx.guild.categories), True),
                ('Cargos', len(ctx.guild.roles), True),
                ('Convites Ativos', len(await ctx.guild.invites()), True),
                ('\u200b', '\u200b', True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('inf')



def setup(bot):
    bot.add_cog(Inf(bot))
