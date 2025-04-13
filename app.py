from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
import threading
from flask import Flask, render_template, request, jsonify
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Configuration ===
BOT_TOKEN = "7626640336:AAGe4CcISfuNP2CcmTy_i0Co9v-mTK9RScw"
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-webapp-url.com")

# === Flask App Setup ===
app = Flask(__name__)
users = {}

# === Initialize Bot and Print Username ===
bot = Bot(BOT_TOKEN)
try:
    bot_info = asyncio.run(bot.get_me())
    print("Bot username:", bot_info.username)
except Exception as e:
    print("Error initializing bot:", e)

# === Flask Routes ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mine", methods=["POST"])
def mine():
    user_id = request.json.get("user_id")
    if user_id not in users:
        users[user_id] = 0.0
    users[user_id] += 0.001
    return jsonify({"message": "You mined 0.001 DOD!", "balance": users[user_id]})

@app.route("/balance", methods=["POST"])
def balance():
    user_id = request.json.get("user_id")
    balance = users.get(user_id, 0.0)
    return jsonify({"balance": balance})

@app.route("/referral", methods=["POST"])
def referral():
    user_id = request.json.get("user_id")
    bot_info = asyncio.run(bot.get_me())
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
    return jsonify({"referral_link": ref_link})

# === Telegram Command Handler ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to DOD Miner Bot! ⛏️\nClick the WebApp button to start mining DOD!"
    )

# === Run Telegram Bot in Background Thread (with asyncio fix) ===
def run_telegram_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())  # ✅ Fix for Python 3.10+
    loop = asyncio.get_event_loop()

    app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start_command))

    loop.run_until_complete(app_telegram.initialize())
    loop.run_until_complete(app_telegram.start())
    loop.run_until_complete(app_telegram.updater.start_polling())
    loop.run_forever()

# === Start Flask Server ===
def start_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# === Main Entry Point ===
if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    start_flask()
