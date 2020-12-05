import random
from typing import Optional

from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command

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

    @command(name='Mandar_Recado', aliases=['Recado','recado'])
    async def recado(self, ctx, member: Member, *, message: Optional[str] = "Bom dia"):
        await ctx.message.delete()
        await ctx.send(f"{ctx.author.display_name} mandou um recado para {member.mention}: {message}")

def setup(bot):
    bot.add_cog(Interacoes(bot))
