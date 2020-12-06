import random
from discord.ext.commands import Cog
from discord.ext.commands import command

class Rpg(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('rpg')


    @command(name='Rolar_Dado', aliases=['d','dado','roll','r'])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split('d'))
        rolls = [random.randint(1, value) for i in range(dice)]
        if dice <= 255 and value <= 255:
            result = (' + '.join([str(r) for r in rolls]) + f' = {sum(rolls)}')
            await ctx.send(result)
        else:
            await ctx.send('Resultado muito grande, Tente um numero menor!')

def setup(bot):
    bot.add_cog(Rpg(bot))
