from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyrogram.handlers import CallbackQueryHandler
from helpers.buttons import ButtonUtils


async def cb_shop(_, callback: CallbackQuery):
    text, button = await ButtonUtils.nokos(0)
    return await callback.edit_message_text(
          text, reply_markup=button
    )


async def cb_page_shop(_, callback: CallbackQuery):
    page = int(callback.matches[0].group(1))
    text, button = await ButtonUtils.nokos(page)
    return await callback.edit_message_text(
          text, reply_markup=button
    ) 


async def open_nokos(client, message):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Open Shop",
                    callback_data="shop"
                )
            ]
        ]
    )

    return await message.reply(
        "Silahkan pilih menu Nokos:",
        reply_markup=buttons,
    )
