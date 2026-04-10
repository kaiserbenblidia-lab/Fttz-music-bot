import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا 👋 اكتب /play اسم الاغنية")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("اكتب اسم الاغنية بعد /play")
        return

    await update.message.reply_text(f"🔎 جاري البحث عن: {query}")

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            url = info['entries'][0]['webpage_url']

        await update.message.reply_text(f"🎵 لقيت:\n{url}")

    except:
        await update.message.reply_text("❌ صار خطأ، جرّب اسم ثاني")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))

app.run_polling()
