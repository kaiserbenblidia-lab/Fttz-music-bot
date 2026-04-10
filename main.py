from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import yt_dlp

TOKEN = "حط_توكنك"

# تخزين أوامر لكل قروب
group_prefix = {}

async def setprefix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("هذا الأمر للجروبات فقط")
        return

    if not context.args:
        await update.message.reply_text("اكتب البادئة الجديدة مثل: /setprefix !")
        return

    prefix = context.args[0]
    group_prefix[update.message.chat.id] = prefix

    await update.message.reply_text(f"تم تغيير الأمر إلى: {prefix}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    text = update.message.text

    prefix = group_prefix.get(chat_id, "!")

    if not text.startswith(prefix):
        return

    query = text.replace(prefix, "").strip()

    if not query:
        return

    await update.message.reply_text("🔎 جاري البحث...")

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        video = info['entries'][0]

        title = video['title']
        url = video['webpage_url']
        thumb = video['thumbnail']

    keyboard = [
        [InlineKeyboardButton("▶️ مشاهدة على يوتيوب", url=url)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=thumb,
        caption=f"🎵 {title}",
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("setprefix", setprefix))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
