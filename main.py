from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token va kanallar
BOT_TOKEN = "8626314578:AAEVCjVqy8ssXv-32WHfu5Vmja5TDf_4JbU"
CHANNELS = {
    "majburiy": "@VEXENPUBGM", 
    "uc": "https://t.me/+dLBaeWMJh9A5YTdi",
    "akk": "https://t.me/+prk0iViTDgc5ZTRi",
    "cheat": "https://t.me/+ptXNKvTbJfliOWEy"
}

# Asosiy menyu
def main_menu():
    return ReplyKeyboardMarkup([
        ['🎁 Tekin UC', '🎮 Tekin Akk'],
        ['🔥 Tekin Cheat'],
        ['📋 Ma\'lumotlar', '🎧 Yordam']
    ], resize_keyboard=True)

# Kanal tekshiruvi
async def is_subscribed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNELS["majburiy"], user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update, context):
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Obuna bo'lish", url=f"https://t.me/{CHANNELS['majburiy'].replace('@', '')}")]])
        await update.message.reply_text("⚠️ Botdan foydalanish uchun kanalimizga obuna bo'ling:", reply_markup=keyboard)
    else:
        await update.message.reply_text("Asosiy menyudasiz! Kerakli bo'limni tanlang:", reply_markup=main_menu())

# Tugmalar funksiyasi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Obunani qayta tekshirish
    if not await is_subscribed(update, context):
        await update.message.reply_text("❌ Iltimos, avval kanalga obuna bo'ling!")
        return

    if text == '🎁 Tekin UC':
        await send_channel_link(update, CHANNELS["uc"], "Tekin UC kanali")
    elif text == '🎮 Tekin Akk':
        await send_channel_link(update, CHANNELS["akk"], "Tekin Akk kanali")
    elif text == '🔥 Tekin Cheat':
        await send_channel_link(update, CHANNELS["cheat"], "Tekin Cheat kanali")
    else:
        await update.message.reply_text("Noto'g'ri tanlov.")

async def send_channel_link(update, url, title):
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}ga o'tish", url=url)]])
    await update.message.reply_text(f"Kerakli {title} pastdagi tugmada:", reply_markup=keyboard)

if __name__ == '__main__':
    # Tokenni to'g'ridan-to'g'ri shu yerda ishlatamiz
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    app.run_polling()