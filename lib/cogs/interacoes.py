import random
from typing import Optional
from datetime import datetime

from discord import Member, Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)
from discord.errors import HTTPException, Forbidden


class Interacoes(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('interacoes')

    @command(name='Duvida', aliases=['duvida'])
    async def duvida(self, ctx, *,die_string: str):
        respostas = ["É certo.",
            "É decididamente assim.",
            "Sem dúvida.",
            "Sim definitivamente.",
            "Você pode contar com ele.",
            "A meu ver, sim.",
            "Provavelmente.",
            "uma boa perspectiva.",
            "Sim.",
            "Sinais apontam que sim.",
            "Resposta nebulosa, tente novamente.",
            "Pergunte novamente mais tarde.",
            "Ainda não formei opinião sobre isso.",
            "Melhor não te dizer agora.",
            "Não é possível prever agora.",
            "Concentre-se e pergunte novamente.",
            "Não conte com isso.",
            "Minha resposta é não.",
            "Não.",
            "Minhas fontes dizem não.",
            "Perspectica não muito boa.",
            "Muito duvidoso."]
        await ctx.send(f'Duvida: {die_string}\nResposta: {random.choice(respostas)}')

    @duvida.error
    async def duvida_error(self, ctx, exc):
        if isinstance(exc, MissingRequiredArgument):
            await ctx.send('É necessario ter uma duvida após o comando, entende?')

    @command(name='Mandar_Recado', aliases=['Recado','recado','Mensagem','mensagem'])
    async def mensagem(self, ctx, member: Member, *, message: Optional[str] = "Bom dia"):
        await ctx.message.delete()
        await ctx.send(f'{member.mention}')
        embed = Embed(title=f"{ctx.author.display_name} mandou um recado para {member.display_name}", description=f'{message}', colour=0x009900, timestamp=datetime.utcnow())
        await ctx.send(embed=embed)

    @mensagem.error
    async def mensagem_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send('Usuario não encontrado, ou mensagem invalida')

def setup(bot):
    bot.add_cog(Interacoes(bot))
