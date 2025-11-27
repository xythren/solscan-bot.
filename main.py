import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get keys from environment variables (safe)
BOT_TOKEN = os.getenv("8491872595:AAGdZ4TsYIq3mfO5DCKZoGlCxtK_YEpNZsA")
SOLSCAN_API_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NjQyMjMwNzQxMDUsImVtYWlsIjoibWFzaHVkYWRhbWFsZWV5dUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJhcGlWZXJzaW9uIjoidjIiLCJpYXQiOjE3NjQyMjMwNzR9.6ed669YlgkYLE2smCww7-uDZ8vfVrrP1xfVh_4PWfak")

# Header for Solscan PRO API
HEADERS = {"token": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3NjQyMjMwNzQxMDUsImVtYWlsIjoibWFzaHVkYWRhbWFsZWV5dUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJhcGlWZXJzaW9uIjoidjIiLCJpYXQiOjE3NjQyMjMwNzR9.6ed669YlgkYLE2smCww7-uDZ8vfVrrP1xfVh_4PWfak}

# ===========================
# TOKEN SCAN COMMAND
# ===========================
async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Use default token if no args or user types "token"
    if len(context.args) == 0 or context.args[0].lower() == "token":
        token_address = "31k88G5Mq7ptbRDf3AM13HAq6wRQHXHikR8hik7wPygk"
    else:
        token_address = context.args[0]

    url = f"https://pro-api.solscan.io/v2.0/token/meta?tokenAddress={token_address}"

    res = requests.get(url, headers=HEADERS).json()

    # Handle API error
    if res.get("status") != "success":
        await update.message.reply_text("❌ Invalid token or Solscan error.")
        return

    data = res["data"]

    # Extract token info
    name = data.get("name", "N/A")
    symbol = data.get("symbol", "N/A")
    decimals = data.get("decimals", "N/A")
    supply = data.get("supply", "N/A")
    verified = "Yes ✅" if data.get("verified") else "No ❌"

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

# ===========================
# RUN BOT
# ===========================
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("scan", scan))

app.run_polling()