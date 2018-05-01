try:
    from mysite.bot_settings import *
except ImportError:
    from mysite.bot_basesettings import *
import pexpect
import subprocess

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

        # pexpect buffer is limited. start loader to avoid overflow. see pexpect spwan maxreadings
        # TODO: Find a clean way to avoid this buffer overflow
        self.log_loader = pexpect.spawn('python3', ["LogLoader.py", str(len(self.bot_outputs))],
                                        cwd="./BotManager/",
                                        encoding='utf-8')

    def _bot_exists(self, index, check_for_instance=True, check_down=False):
        if index not in range(0, len(BotManager.bots), 1):
            return False
        if check_for_instance and self.bot_instances[index] is None:
            return False
        if check_down and self.bot_instances[index] is not None:
            if not self.bot_instances[index].is_alive:
                return False
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

    def get_log_loader_output(self):
        bot = self.log_loader
        # read as long as there is new input
        output = ""
        while True:
            try:
                output += bot.read_nonblocking(100, timeout=0)
            except pexpect.TIMEOUT:
                break

        return output

    def get_bot_status(self, index):
        if not self._bot_exists(index):
            return False

        bot = self.bot_instances[index]
        return bot.isalive()

    def get_all_status(self):
        status = []
        for bot in self.bot_instances:
            if bot is None:
                status.append(False)
            else:
                status.append(bot.isalive())
        return status

    def get_bot_list(self):
        bot_list = []
        for bot in self.bots:
            bot_list.append(bot)
        return bot_list

    def clear_bot_output(self, index):
        if not self._bot_exists(index):
            return False

        self.bot_outputs[index] = ''

        return True

    def git_pull_bot(self, index):
        if not self._bot_exists(index, check_for_instance=False):
            return False

        try:
            return(subprocess.check_output(['git', 'pull'],
                                           stderr=subprocess.STDOUT,
                                           cwd=self.bots[index].path))
        except subprocess.CalledProcessError as non_zero_return:
            return b'Pull not successfull:\n' + non_zero_return.output


