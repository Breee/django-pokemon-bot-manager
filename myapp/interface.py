import discord
from discord.ext import commands


class BotInterface:

    def __init__(self):
        self.bot = commands.Bot(description="Test 2", command_prefix=("!raid-", "!r-"))
        self.token = 'NDExNTM5NTY4Mjg2NzYwOTcw.DV9MNA.iKa3qlTDObDYo5EG_F0kDaLCVvU'

    def start_bot(self):
        print('Try starting bot...')
        self.bot.run(self.token)

    def stop_bot(self):
        self.bot.close()
