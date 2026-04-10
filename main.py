from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "PUT_YOUR_TOKEN_HERE"

# البحث فقط بدون تحميل
def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        video = info['entries'][0]
        return video['title'], video['webpage_url']

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text.startswith("!"):
        song_name = text.replace("!", "")

        await update.message.reply_text("🔍 جاري البحث...")

        try:
            title, url = search_youtube(song_name)

            keyboard = [
                [InlineKeyboardButton("▶️ فتح في يوتيوب", url=url)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # إرسال الرابط (تيليجرام يحوله لمشغل)
            await update.message.reply_text(
                f"🎵 {title}\n{url}",
                reply_markup=reply_markup,
                disable_web_page_preview=False  # مهم عشان يظهر المشغل
            )

        except:
            await update.message.reply_text("❌ ما حصلت الأغنية")

    elif text == "!العاب":
        await update.message.reply_text("🎮 جرب:\n- !اسئلني\n- قريبًا ألعاب أكثر 😄")

    elif text == "!اسئلني":
        await update.message.reply_text("❓ وش أكثر شيء تحبه في يومك؟")

    else:
        await update.message.reply_text("اكتب !اسم_الأغنية 🎧")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
