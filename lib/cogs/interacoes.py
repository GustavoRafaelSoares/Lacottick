import random
import discord
from discord.ext.commands import Cog

class Interacoes(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('interacoes')
'''
    @Cog.command()
    async def duvida(self, ctx, *, pergunta):
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
            "Pespectica não muito boa.",
            "Muito duvidoso."]
        await ctx.send(f'Duvida: {pergunta}\nResposta: {random.choice(respostas)}')

    @duvida.error
    async def duvida_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Depois do comando tem que ter a duvida meu caro. Se não não tem o que eu responder')
'''
def setup(bot):
    bot.add_cog(Interacoes(bot))
