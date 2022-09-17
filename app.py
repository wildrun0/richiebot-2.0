from loader import bot, daily_tasks, lh
import events

def main():
    bot.loop_wrapper = daily_tasks.lw
    bot.loop_wrapper.add_task(lh.relocate_logs())

    bot.run_forever()

if __name__=='__main__':
    main()