import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8491872595:AAGdZ4TsYIq3mfO5DCKZoGlCxtK_YEpNZsA")
SOLSCAN_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NjQyMjMwNzQxMDUsImVtYWlsIjoibWFzaHVkYWRhbWFsZWV5dUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJhcGlWZXJzaW9uIjoidjIiLCJpYXQiOjE3NjQyMjMwNzR9.6ed669YlgkYLE2smCww7-uDZ8vfVrrP1xfVh_4PWfak")
ADMIN_USER_ID = 5421158872  # <-- Your Telegram user ID

if not BOT_TOKEN or not SOLSCAN_API_KEY:
    raise EnvironmentError("Missing BOT_TOKEN or SOLSCAN_API_KEY in environment variables.")

HEADERS = {"token": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NjQyMjMwNzQxMDUsImVtYWlsIjoibWFzaHVkYWRhbWFsZWV5dUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJhcGlWZXJzaW9uIjoidjIiLCJpYXQiOjE3NjQyMjMwNzR9.6ed669YlgkYLE2smCww7-uDZ8vfVrrP1xfVh_4PWfak}

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0 or context.args[0].lower() == "token":
        token_address = "31k88G5Mq7ptbRDf3AM13HAq6wRQHXHikR8hik7wPygk"
    else:
        token_address = context.args[0]

    url = f"https://pro-api.solscan.io/v2.0/token/meta?tokenAddress={token_address}"

    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        data = res.json()
    except Exception:
        await update.message.reply_text("❌ Error contacting Solscan API.")
        return

    if data.get("status") != "success":
        await update.message.reply_text("❌ Invalid token or Solscan error.")
        return

    token_data = data["data"]

    name = token_data.get("name", "N/A")
    symbol = token_data.get("symbol", "N/A")
    decimals = token_data.get("decimals", "N/A")
    supply = token_data.get("supply", "N/A")
    verified = "Yes ✅" if token_data.get("verified") else "No ❌"

    solscan_link = f"https://solscan.io/token/{token_address}"

    msg = (
        f"📌 *TOKEN SCAN RESULT*\n\n"
        f"💠 *Name:* {name}\n"
        f"🔹 *Symbol:* {symbol}\n"
        f"🔢 *Decimals:* {decimals}\n"
        f"📦 *Supply:* {supply}\n"
        f"✔️ *Verified:* {verified}\n\n"
        f"🔗 {solscan_link}"
    )

    await update.message.reply_text(msg, parse_mode="Markdown")
    # Also send to admin (you), unless you ran the command yourself
    if update.effective_user.id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=ADMIN_USER_ID, text=msg, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("scan", scan))
app.run_polling()
