from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "PUT_YOUR_TOKEN_HERE"

# تحميل الأغنية
def download_song(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        video = info['entries'][0]
        file_name = ydl.prepare_filename(video)
        return file_name, video['title'], video['webpage_url']

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text.startswith("!"):
        song_name = text.replace("!", "")

        msg = await update.message.reply_text("⏳ جاري تحميل الأغنية...")

        try:
            file_path, title, url = download_song(song_name)

            # زر يوتيوب
            keyboard = [
                [InlineKeyboardButton("▶️ فتح في يوتيوب", url=url)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # إرسال الصوت
            with open(file_path, 'rb') as audio:
                await update.message.reply_audio(
                    audio=audio,
                    title=title,
                    reply_markup=reply_markup
                )

            await msg.delete()

            # حذف الملف بعد الإرسال
            os.remove(file_path)

        except Exception as e:
            await update.message.reply_text("❌ صار خطأ أثناء تحميل الأغنية")

    else:
        await update.message.reply_text("اكتب !اسم_الأغنية 🎧")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
