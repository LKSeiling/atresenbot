import logging
import datetime as dt
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, GROUP_ID, TIMEZONE
from handlers.group import handle_group_message
from handlers.private import show_tops
from handlers.admin import admin_add, admin_remove, bot_on, bot_off, bot_enabled
from jobs.reminder import send_reminder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def guard_group(update, context):
    if not bot_enabled():
        return
    await handle_group_message(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(MessageHandler(filters.Chat(GROUP_ID) & filters.TEXT, guard_group))
    app.add_handler(CommandHandler("tops", show_tops))
    app.add_handler(CommandHandler("admin_add", admin_add))
    app.add_handler(CommandHandler("admin_remove", admin_remove))
    app.add_handler(CommandHandler("bot_on", bot_on))
    app.add_handler(CommandHandler("bot_off", bot_off))

    # Jobs (täglich 10:00 in konfigurierte Zeitzone)
    reminder_time = dt.time(hour=10, minute=0, tzinfo=TIMEZONE)
    app.job_queue.run_daily(send_reminder, reminder_time)

    logger.info("Starte Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()

