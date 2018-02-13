from discord.ext import commands
import discord
import datetime
import aiohttp


class PollBot(commands.Bot):
    def __init__(self):
        pass

    def myinit(self, prefix, description, token):
        super().__init__(command_prefix=prefix, description=description, pm_help=None, help_attrs=dict(hidden=True))
        self.token = token
        self.uptime = 0
        self.add_command(self.ping)
        self.session = aiohttp.ClientSession(loop=self.loop)


    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(self.uptime)

    def run(self):
        super().run(self.token)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_resumed(self):
        print('resumed...')

    @commands.command(hidden=True)
    async def ping(self):
        await self.say("pong!")

    def get_dict(self):
        return {'lalal': 1, 'lalal1': 2}
