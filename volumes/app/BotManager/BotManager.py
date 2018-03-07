from collections import namedtuple
from multiprocessing import Process
import importlib.util
import os
import sys



class BotManager:
    '''
        struct for defining bots
        name: name of the bots class
        config: configs for the bot
        path: path to the bots files
        main_file: main python file of the bot e.g. 'Bot.py'
    '''
    BotStruct = namedtuple("BotStruct", "name config path main_file")

    # define bots
    bots = [BotStruct(name="PollBot",
                      config={'prefix': '!raid', 'description': 'Raidquaza',
                              'config_file': '/home/lukas/src/pokemon-raid-bot/config.conf'},
                      path="/home/lukas/src/pokemon-raid-bot",
                      main_file='pollbot/PollBot.py')]

    def __init__(self):
        self.bot_instances = []
        self.processes = []
        self.pid = 0
        for bot_struct in BotManager.bots:
            if not bot_struct.path.startswith('/'):
                path = '/' + os.path.relpath(os.getcwd() + '/../' + bot_struct.path, '/')
            else:
                path = bot_struct.path

            # add bot path to sys path to make usage of submodules possible
            sys.path.append(path)

            spec = importlib.util.spec_from_file_location(bot_struct.name,
                                                          path + '/' + bot_struct.main_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            instance = getattr(module,
                               bot_struct.name)(bot_struct.config['prefix'],
                                                bot_struct.config['description'],
                                                bot_struct.config['config_file'])
            self.bot_instances.append(instance)

            self.processes.append(None)

    def get_bot(self, index):
        if index not in range(0, len(BotManager.bots), 1):
            return None
        return self.bot_instances[index]

    def run_bot(self, index):
        if index not in range(0, len(BotManager.bots), 1):
            return None

        def bot_runner(bot, pid):
            import os
            pid = os.getpid()
            print(pid)
            bot.run()

        bot = self.bot_instances[index]
        self.processes[index] = Process(target=bot_runner, args=[bot, self.pid])
        self.processes[index].start()
        print(self.pid)

    def close_bot(self, index):
        if index not in range(0, len(BotManager.bots), 1):
            return
        self.processes[index].terminate()
        print(self.pid)
        self.processes[index].join()
