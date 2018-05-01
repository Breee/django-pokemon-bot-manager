#!/usr/bin/python3

from BotManager import BotManager
import time

bm = BotManager()
run = bm.run_bot(0)

print(run)
time.sleep(5)
print('close?')
input()
bm.close_bot(0)
print('close')
time.sleep(5)
