import datetime as dt
from utils.storage import load_json
from config import GROUP_ID, PLENUM_WEEKDAY, TOPS_FILE

async def send_reminder(context):
    tomorrow = dt.date.today() + dt.timedelta(days=1)
    if tomorrow.strftime("%A") == PLENUM_WEEKDAY:
        tops = load_json(TOPS_FILE, {})
        month = tomorrow.isoformat()[:7]
        if month in tops and tops[month]:
            text = "📝 TOPs für das morgige Plenum:\n" + "\n".join(
                f"- {t['text']} ({t['user']})" for t in tops[month]
            )
        else:
            text = "Keine TOPs für diesen Monat."
        await context.bot.send_message(chat_id=GROUP_ID, text=text)