from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
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

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(782303967325192230)
            print('Lacottick esta preparado')
        else:
            print('lacottick reconectado')

    async def on_message(self, message):
        pass

bot = Bot()
