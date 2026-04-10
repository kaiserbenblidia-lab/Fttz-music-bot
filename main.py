import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "PUT_YOUR_TOKEN_HERE"

users_money = {}

# 💰 نظام الفلوس
def get_money(user_id):
    if user_id not in users_money:
        users_money[user_id] = 100
    return users_money[user_id]

def add_money(user_id, amount):
    users_money[user_id] = get_money(user_id) + amount

# 🎵 تشغيل أغنية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # !play
    if text.startswith("!play"):
        song = text.replace("!play", "").strip()

        if not song:
            await update.message.reply_text("❌ Please write a song name.\nExample: !play Shape of You")
            return

        await update.message.reply_text("🔎 Searching...")

        ydl_opts = {'format': 'bestaudio', 'quiet': True}

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song}", download=False)
            video = info['entries'][0]
            title = video['title']
            url = video['webpage_url']

        # زر يوتيوب
        keyboard = [
            [InlineKeyboardButton("▶️ Watch on YouTube", url=url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        add_money(user_id, 10)

        await update.message.reply_text(
            f"🎵 {title}\n\n💰 You earned 10 coins!",
            reply_markup=reply_markup
        )

    # 💰 فلوسي
    elif text == "!money":
        money = get_money(user_id)
        await update.message.reply_text(f"💰 You have {money} coins")

    # 🎁 يومي
    elif text == "!daily":
        add_money(user_id, 50)
        await update.message.reply_text("🎁 You got 50 coins!")

    # 🤖 ردود بسيطة
    elif text == "!help":
        await update.message.reply_text(
            "🤖 Commands:\n"
            "!play song\n"
            "!money\n"
            "!daily\n"
            "!help"
        )

    else:
        await update.message.reply_text("❓ Unknown command. Type !help")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
