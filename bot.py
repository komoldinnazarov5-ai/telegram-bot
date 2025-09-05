from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = 27863250
API_HASH = "2e248f7f649f9a74f817f789764caac7"
BOT_TOKEN = "8207279220:AAG6muzDTbw7_FxGpFs74cnG0ILRFGHAA2Y"

ADMIN_ID = 5716998281
CHANNEL_ID = -1001780955762
CHANNEL_LINK = "https://t.me/Ani_Major"

bot = Client("anime_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Anime qismlarni hisoblash uchun counter
episode_counter = {}

# Start komandasi
@bot.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.reply_text(
            "👋 Salom! Botdan foydalanish uchun kanalimizga obuna bo‘ling:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📺 Kanalga obuna bo‘lish", url=CHANNEL_LINK)]]
            ),
        )
    else:
        await message.reply_text("👋 Salom Admin! Sizga xush kelibsiz.")

# Admin yuborgan bannerlarni kanalga chiqarish
@bot.on_message(filters.photo & filters.user(ADMIN_ID))
async def send_banner(client, message):
    caption = message.caption or "📺 Yangi Anime!"
    await bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=message.photo.file_id,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("▶️ Tomosha qilish", url=f"t.me/{client.me.username}?start=anime")]]
        )
    )
    await message.reply_text("✅ Banner kanalga joylandi.")

# Admin yuborgan videolarni kanalga chiqarish (raqam bilan)
@bot.on_message(filters.video & filters.user(ADMIN_ID))
async def send_video(client, message):
    # Har bir anime uchun alohida counter
    anime_key = "default"  
    if anime_key not in episode_counter:
        episode_counter[anime_key] = 1
    else:
        episode_counter[anime_key] += 1

    caption = f"🎬 {episode_counter[anime_key]}-qism"
    if message.caption:
        caption += f"\n{message.caption}"

    await bot.send_video(
        chat_id=CHANNEL_ID,
        video=message.video.file_id,
        caption=caption
    )
    await message.reply_text(f"✅ {episode_counter[anime_key]}-qism kanalga joylandi.")

print("🤖 Bot ishga tushdi...")
bot.run()
