from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from apps.core import db


class Paginates:
    @staticmethod
    async def nokos(page: int):
        list_nokos = await db.get_nokos() 
        if not list_nokos:
            return

        items_page = 4
        total_items = len(prtc)
        max_pages = ceil(
            total_items / items_page
        )
        page = max(0, min(page, max_pages - 1))
    
        start = page * items_page
        end = start + items_page
        current_items = prtc[start:end]

        text = f"<b>Nokos List! ({total_items})</b> ({page + 1}/{max_pages})\n\n"

        buttons = []
        selection_row = []
    
        for num, doc in enumerate(current_items, start=start + 1):
            _id = doc.get("_id")
            price = doc.get("price")

            text += f"<b>{num} - Noktel</b>\n"
            text += f"<b> IDs: <code>{_id}</code>\n Price: <code>{price}</code></b>\n\n"

            selection_row.append(
                InlineKeyboardButton(
                    text=str(num), callback_data=f"buy_id_{_id}"
                )
            )
        
        if selection_row:
            buttons.append(selection_row)
        
        nav_row = []
        if page > 0:
            nav_row.append(
                InlineKeyboardButton(
                    "<×",  callback_data=f"list_nokos_{page - 1}"
                ),
            )

        nav_row.append(
            InlineKeyboardButton("Back", callback_data="back_menu")
        )
    
        if page < max_pages - 1:
            nav_row.append(
                InlineKeyboardButton(
                    "×>", callback_data=f"list_nokos_{page + 1}"
                )
            )
    
        if nav_row:
            buttons.append(nav_row)
        return text, InlineKeyboardMarkup(buttons)


