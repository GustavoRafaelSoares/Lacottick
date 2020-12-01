from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord import Embed, File
from discord import Intents

PREFIX = 'l.'
OWNER_IDS = [543121839988408334]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
            )

    def run(self, version):
        self.VERSION = version

        with open('./lib/bot/token.0','r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print('Lacottick esta executando...')
        super().run(self.TOKEN, reconnect=True)
    async def on_connect(self):
        print('lacottick conectado')

    async def on_disconect(self):
        print('lacottick desconectado')

    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send('Algo deu errado...')

        else:
            channel = self.get_channel(782303967325192234)
            await channel.send('Um erro ocorreu durante a execução...')
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, commandNotFound):
            pass
        elif hasattr(exc, 'original'):
            raise exc.original
        else:
            raise exc
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(782303967325192230)
            print('Lacottick esta pronto')

            channel = self.get_channel(782303967325192234)
            await channel.send('Estou Online!')

            embed = Embed(title='Estou Online!',description='Agora voce pode usar o bot como quiser!', colour=0x009900, timestamp=datetime.utcnow())
            fields = [('Versão',self.VERSION,False),
            ('Ainda em Desenvolvimento','Estamos trabalhando arduamente para que seja finalizado logo',False),
            ('Contato', 'Chama no pv para reportar um bug ou tirar uma duvida', False)]
            for name,value, inline in fields:
                embed.add_field(name=name,value=value,inline=inline)
            embed.set_footer(text='Lacottick ainda sera o seu bot de respeito...')
            embed.set_author(name='Lacottick', icon_url='')
            #embed.set_thumbnail(url='')
            #embed.set_image(url='')
            await channel.send(embed=embed)

            await channel.send(file=File('./data/images/icon.png'))
        else:
            print('lacottick reconectado')

    async def on_message(self, message):
        pass

bot = Bot()
