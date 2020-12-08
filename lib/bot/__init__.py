from asyncio import sleep
from datetime import datetime
from glob import glob
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext.commands import Context
from discord.errors import HTTPException, Forbidden
from discord import Embed, File
from discord import Intents

from ..db import db

PREFIX = 'l.'
OWNER_IDS = [543121839988408334]
COGS = [path.split(os.sep)[-1][:-3] for path in glob('./lib/cogs/*.py')]
IGNORE_EXCEPTION = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'    {cog} - Pronto')

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
            )

    def setup(self):
        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}')
            print(f'    cog: {cog} - carregado')
        print('setup completo')

    def run(self, version):
        self.VERSION = version

        print('Iniciando setup...')
        self.setup()

        with open('./lib/bot/token.0','r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print('Lacottick esta executando...')
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx  = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send('Ainda não estou pronto para receber comandos, espere alguns segundos...')

    async def rules_reminder(self):
        embed = Embed(title='Ei você',description='Lembre-se das regras!', colour=0x009900, timestamp=datetime.utcnow())
        await self.stdout.send(embed=embed)

    async def on_connect(self):
        print('lacottick conectado')

    async def on_disconect(self):
        print('lacottick desconectado')

    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send('Isso deve estar errado...')

        await self.stdout.send('Um erro ocorreu durante a execução...')
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTION]):
            pass
        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f'O comando esta em cooldown, tente denovo em: {exc.retry_after:,.2f} segundos.')
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send('Um ou mais argumentos são requeridos para esta ação')
        elif isinstance(exc.original, HTTPException):
            await cxt.send('Não é possivel enviar mensagens')
        elif isinstance(exc.origianl, Forbidden):
            await cxt.send('Não tenho as permissões necessarias')
        elif hasattr(exc, 'original'):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(782303967325192230)
            self.stdout = self.get_channel(784454139040104468)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(hour=12, minute=0, second=10))
            self.scheduler.start()

            await self.stdout.send('Estou Online!')

            embed = Embed(title='Estou Online!',description='Agora voce pode usar o bot como quiser!', colour=0x009900, timestamp=datetime.utcnow())
            fields = [('Versão',self.VERSION,False),
            ('Ainda em Desenvolvimento','Estamos trabalhando arduamente para que seja finalizado logo',False),
            ('Host','heroku.com',False),
            ('Contato', 'Chama no pv para reportar um bug ou tirar uma duvida', False)]
            for name,value, inline in fields:
                embed.add_field(name=name,value=value,inline=inline)
            embed.set_footer(text='Lacottick ainda sera o seu bot de respeito...')
            embed.set_author(name='Lacottick', icon_url='')
            embed.set_thumbnail(url='')
#            embed.set_image(url='')
            await self.stdout.send(embed=embed)

#            await channel.send(file=File('./data/images/icon.png'))
            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print('Lacottick esta pronto')
        else:
            print('lacottick reconectado')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()
