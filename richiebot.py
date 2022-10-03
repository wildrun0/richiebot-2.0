#!/usr/bin/python
from loader import bot, daily_tasks
import events

def main():
    bot.loop_wrapper = daily_tasks.lw
    bot.run_forever()

if __name__=='__main__':
    main()