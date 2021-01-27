import random
from typing import Optional
from datetime import datetime

from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)
from discord.errors import HTTPException, Forbidden


class Interacoes(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('interacoes')

    @command(name='Duvida', aliases=['duvida'],brief="Este comando retorna uma resposta para sua duvida")
    @cooldown(2, 60, BucketType.user)
    async def duvida(self, ctx, *,duvida: str):
        respostas = ["É certo.",
            "É decididamente assim.",
            "Sem dúvida.",
            "Pode ser",
            "Dizem que sim",
            "Nicolinos me proibiu de dar esta resposta",
            "Sim definitivamente.",
            "Você pode contar com isso.",
            "Você pode contar comigo.",
            "A meu ver, sim.",
            "Provavelmente.",
            "uma boa perspectiva.",
            "Sim.",
            "Sinais apontam que sim.",
            "Não to afim de falar sobre isso",
            "Ainda não formei opinião sobre isso.",
            "Melhor não te dizer agora.",
            "Não é possível prever agora.",
            "Não conte com isso.",
            "Minha resposta é não.",
            "Não.",
            "Minhas fontes dizem não.",
            "Perspectica não muito boa.",
            "Muito duvidoso.",
            "ta mec",
            "trotos",
            "é troll",
            "dale, dele, doly",
            "Quem sabe né...",
            "Duvido",
            "Duvidoso",
            "Duvido Muito"]
        await ctx.send(f'Duvida: {duvida}\nResposta: {random.choice(respostas)}')

    @duvida.error
    async def duvida_error(self, ctx, exc):
        if isinstance(exc, MissingRequiredArgument):
            await ctx.send('É necessario ter uma duvida após o comando, entende?')

    @command(name='Mandar_Recado', aliases=['recado'], brief="Este comando marca a pessoa e a apresenta a mensagem")
    async def mensagem(self, ctx, member: Member, *, menssagem: Optional[str] = "Bom dia"):
        await ctx.message.delete()
        await ctx.send(f'{member.mention}')
        embed = Embed(title=f"{ctx.author.display_name} mandou um recado para {member.display_name}", description=f'{menssagem}', colour=0x009900, timestamp=datetime.utcnow())
        await ctx.send(embed=embed)

    @command(name='Pergunta', aliases=[''])
    async def pergunta(self, ctx, ): #pergunta aleatoria com resposta simpes (sim,não)
        pass

#interações avançadas nivel ZT, chorar gritar etc..
#assuntos do momento
#ia de chat
#memes aleatorios
#mensagem de jogando, vendo etc...

    @mensagem.error
    async def mensagem_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send('Usuario não encontrado, ou mensagem invalida')

def setup(bot):
    bot.add_cog(Interacoes(bot))
