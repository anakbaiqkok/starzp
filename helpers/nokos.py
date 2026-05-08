from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyrogram.handlers import CallbackQueryHandler
from helpers.buttons import nokos


async def cb_shop(_, callback: CallbackQuery):
    text, button = await Buttonutils.nokos(0)
    return await callback.edit_message_text(
          text, reply_markup=button
    )


async def cb_page_shop(_, callback: CallbackQuery):
    page = int(callback.matches[0].group(1))
    text, button = await Buttonutils.nokos(page)
    return await callback.edit_message_text(
          text, reply_markup=button
    ) 


Handlers.command["bot"].update({
    "cb_shop": CallbackQueryHandler(
        cb_shop, filters.regex(r"^shop$")
    ),
    "cb_page_shop": CallbackQueryHandler(
        cb_page_shop, filters.regex(r"^list_nokos_(\d+)")
    ) 
})


