from discord import Embed
from typing import Optional
from discord.ext.menus import MenusPages, ListPageSource
from discord.utils import get
from discord.ext.commands import Cog
from discord.ext.commands import commands

def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ('self', 'ctx'):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")
    params = " ".join(params)

    return f"'''{cmd_and_aliases} {params}'''"

class HelpMenu(ListPageSource):
    def __init__(self):
        self.ctx = ctx
        super().__init__(data, per_page=3)

    async def write_page(self, menus, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title='',
                      description='',
                      colour=self.ctx.author.colour,)
        embed.set_thumbnail(url='')
        embed.set_footer(text=f'')

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((command.brief or "sem descrição", synstax(command)))

        return self.write_page(menu, fields)

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Ajuda com '{command}'",
                      description=synstax(command),
                      colour=ctx.author.colour)
        embed.add_field(name='Descrição:',value=command.help)
        await ctx.send(embed=embed)


    @command(name='help', aliases=['ajuda'])
    async def show_help(self, ctx, cmd: Optional[str]):
        """Mostra esta mensagem!""
        #brief = "Mostra esta mensagem!"
        if cmd is None:
            pass
        else:
            if (command := get(self.bot.commands, name=cmd)): #Deve ta faltando algo aqui...
                await self.cmd_help(ctx, command)
            else:
                await ctx.send('Este comando não existe em minha biblioteca.')

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('Help')

def setup(bot):
    bot.add_cog(Help(bot))
