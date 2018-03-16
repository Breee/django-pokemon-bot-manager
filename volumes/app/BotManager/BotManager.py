from mysite.settings import *
import pexpect
from collections import namedtuple

BotStruct = namedtuple("BotStruct", "path main_file name")


class BotManager:
    """
        struct for defining bots
        name: name of the bots class
        config: configs for the bot
        path: path to the bots files
        main_file: main python file of the bot e.g. 'Bot.py'
    """
    # define bots
    bots = BOTS

    def __init__(self):
        self.bot_instances = []
        self.bot_outputs = []
        for bot_struct in BotManager.bots:
            self.bot_instances.append(None)
            self.bot_outputs.append('')

    def _bot_exists(self, index):
        if index not in range(0, len(BotManager.bots), 1) or self.bot_instances[index] is None:
            return False
        else:
            return True

    def run_bot(self, index):
        if index not in range(0, len(BotManager.bots), 1):
            return False

        bot = self.bots[index]
        self.bot_instances[index] = pexpect.spawn('python3', [bot.main_file], cwd=bot.path,
                                                  encoding='utf-8')
        return True

    def close_bot(self, index):
        if not self._bot_exists(index):
            return False

        bot = self.bot_instances[index]

        bot.sendcontrol('c')
        return True

    def kill_bot(self, index):
        if not self._bot_exists(index):
            return False

        bot = self.bot_instances[index]
        bot.sendcontrol('c')
        return True

    def get_bot_output(self, index):
        if not self._bot_exists(index):
            return False

        bot = self.bot_instances[index]
        # read as long as there is new input
        while True:
            try:
                self.bot_outputs[index] += bot.read_nonblocking(100, timeout=0)
            except pexpect.TIMEOUT:
                break

        return self.bot_outputs[index]

    def get_bot_status(self, index):
        if not self._bot_exists(index):
            return False

        bot = self.bot_instances[index]
        return bot.isalive()

    def get_bot_list(self):
        bot_list = []
        for bot in self.bots:
            bot_list.append(bot.name)
        return bot_list

