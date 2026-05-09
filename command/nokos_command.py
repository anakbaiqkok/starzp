from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.handlers import CallbackQueryHandler
from helpers.buttons import ButtonUtils


async def cb_shop(_, callback: CallbackQuery):
    category_id = callback.data.split()
    text, button = await ButtonUtils.nokos(0, category_id[1])
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
                    "id 1",
                    callback_data="shop 1"
                )
            ]
        ]
    )

    return await message.reply(
        "Silahkan pilih menu Nokos:",
        reply_markup=buttons,
    )


async def open_nokos_cb(_, callback: CallbackQuery):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "id 1",
                    callback_data="shop 1"
                )
            ]
        ]
    )

    return await callback.edit_message_text(
        "Silahkan pilih menu Nokos:",
        reply_markup=buttons,
    )
