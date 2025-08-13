import logging
import datetime as dt
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, WEBHOOK_URL, PORT, LISTEN_ADDR, GROUP_ID, TIMEZONE
from handlers.group import handle_group_message
from handlers.private import show_tops
from handlers.admin import admin_add, admin_remove, bot_on, bot_off, bot_enabled
from jobs.reminder import send_reminder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def guard_group(update, context):
    # Ignoriere Gruppen-Nachrichten, wenn Bot deaktiviert ist
    if not bot_enabled():
        return
    await handle_group_message(update, context)

def build_app() -> Application:
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

    return app

if __name__ == "__main__":
    app = build_app()
    logger.info("Starte Webhook...")
    app.run_webhook(
        listen=LISTEN_ADDR,
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{BOT_TOKEN}",
    )