from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_json
from config import TOPS_FILE

def _format_tops(tops: dict) -> str:
    if not tops:
        return "Keine TOPs gespeichert."
    lines = ["📅 Gespeicherte TOPs:"]
    for month in sorted(tops.keys()):
        entries = tops[month]
        if not entries:
            continue
        lines.append(f"\n🔹 {month}:")
        for e in entries:
            lines.append(f"- {e['text']} ({e['date']}, {e['user']})")
    return "\n".join(lines)

async def show_tops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return
    tops = load_json(TOPS_FILE, {})
    await update.effective_message.reply_text(_format_tops(tops))