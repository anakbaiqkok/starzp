from pyrogram import filters
from pyrogram.helpers import ikb, kb
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
from helpers.buttons import ButtonUtils


async def cb_shop(_, callback: CallbackQuery):
    category_id = callback.data.split()[1]

    text, button = await ButtonUtils.nokos(
        0,
        category_id
    )

    return await callback.edit_message_text(
        text,
        reply_markup=button
    )


async def cb_page_shop(_, callback: CallbackQuery):
    data = callback.data.split("_")

    page = int(data[2])
    category_id = data[3]

    if category_id == "all":
        category_id = None

    text, button = await ButtonUtils.nokos(
        page,
        category_id
    )

    return await callback.edit_message_text(
        text,
        reply_markup=button
    )


async def open_nokos(client, message):
    text = """
<blockquote><b>📱 Beli Akun Telegram</b></blockquote>

📦 <b>Cek Stok</b> — Ketersediaan per tipe ID
📋 <b>Peraturan</b> — Baca sebelum beli
🧾 <b>Riwayat</b> — Histori transaksi Anda
🛒 <b>Order Akun</b> — Beli sekarang

<i>Beli akun Telegram siap pakai.</i>
"""

    buttons = kb(
        [
            [
                "📦 Cek Stok",
                "📋 Peraturan",
            ],
            [
                "🧾 Riwayat",
                "🛒 Order Akun",
            ],
            [
                "🏠 Beranda"
            ]
        ],
        resize_keyboard=True
    )

    return await message.reply(
        text,
        reply_markup=buttons,
    )


async def open_nokos_cb(_, callback: CallbackQuery):
    text = """
<blockquote><b>📱 Beli Akun Telegram</b></blockquote>

📦 <b>Cek Stok</b> — Ketersediaan per tipe ID
📋 <b>Peraturan</b> — Baca sebelum beli
🧾 <b>Riwayat</b> — Histori transaksi Anda
🛒 <b>Order Akun</b> — Beli sekarang

<i>Beli akun Telegram siap pakai.</i>
"""

    return await callback.edit_message_text(text)
