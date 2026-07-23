import os
from io import BytesIO

import aiofiles
import aiohttp
import aiohttp
import base64

from config import BOT_NAME

from .tools import Tools


class QuotlyException(Exception):
    pass


class Quotly:
    GAMBAR_KONTOL = """
⣠⡶⠚⠛⠲⢄⡀
⣼⠁ ⠀⠀⠀ ⠳⢤⣄
⢿⠀⢧⡀⠀⠀⠀⠀⠀⢈⡇
⠈⠳⣼⡙⠒⠶⠶⠖⠚⠉⠳⣄
⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄
⠀⠀⠀⠘⣆ ⠀⠀⠀⠀ ⠀⠈⠓⢦⣀
⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠲⢤
⠀⠀⠀⠀⠀⠀⠙⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧
⠀⠀⠀⠀⠀⠀⠀⡴⠋⠓⠦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠈⣇
⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄
⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⠀⠀⠀⠀⠀⠀⢹⡄⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃
⠀⠀⠀⠀⠀⠀⠀⠙⢦⣀⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⢦⣀⣀⣀⣀⣠⡴⠚⠉
"""

    GAMBAR_TITIT = """
😋😋
😋😋😋
  😋😋😋
    😋😋😋
     😋😋😋
       😋😋😋
        😋😋😋
         😋😋😋
          😋😋😋
          😋😋😋
      😋😋😋😋
 😋😋😋😋😋😋
 😋😋😋  😋😋😋
    😋😋       😋😋
"""
    colors = [
        "White",
        "Navy",
        "DarkBlue",
        "MediumBlue",
        "Blue",
        "DarkGreen",
        "Green",
        "Teal",
        "DarkCyan",
        "DeepSkyBlue",
        "DarkTurquoise",
        "MediumSpringGreen",
        "Lime",
        "SpringGreen",
        "Aqua",
        "Cyan",
        "MidnightBlue",
        "DodgerBlue",
        "LightSeaGreen",
        "ForestGreen",
        "SeaGreen",
        "DarkSlateGray",
        "DarkSlateGrey",
        "LimeGreen",
        "MediumSeaGreen",
        "Turquoise",
        "RoyalBlue",
        "SteelBlue",
        "DarkSlateBlue",
        "MediumTurquoise",
        "Indigo  ",
        "DarkOliveGreen",
        "CadetBlue",
        "CornflowerBlue",
        "RebeccaPurple",
        "MediumAquaMarine",
        "DimGray",
        "DimGrey",
        "SlateBlue",
        "OliveDrab",
        "SlateGray",
        "SlateGrey",
        "LightSlateGray",
        "LightSlateGrey",
        "MediumSlateBlue",
        "LawnGreen",
        "Chartreuse",
        "Aquamarine",
        "Maroon",
        "Purple",
        "Olive",
        "Gray",
        "Grey",
        "SkyBlue",
        "LightSkyBlue",
        "BlueViolet",
        "DarkRed",
        "DarkMagenta",
        "SaddleBrown",
        "DarkSeaGreen",
        "LightGreen",
        "MediumPurple",
        "DarkViolet",
        "PaleGreen",
        "DarkOrchid",
        "YellowGreen",
        "Sienna",
        "Brown",
        "DarkGray",
        "DarkGrey",
        "LightBlue",
        "GreenYellow",
        "PaleTurquoise",
        "LightSteelBlue",
        "PowderBlue",
        "FireBrick",
        "DarkGoldenRod",
        "MediumOrchid",
        "RosyBrown",
        "DarkKhaki",
        "Silver",
        "MediumVioletRed",
        "IndianRed ",
        "Peru",
        "Chocolate",
        "Tan",
        "LightGray",
        "LightGrey",
        "Thistle",
        "Orchid",
        "GoldenRod",
        "PaleVioletRed",
        "Crimson",
        "Gainsboro",
        "Plum",
        "BurlyWood",
        "LightCyan",
        "Lavender",
        "DarkSalmon",
        "Violet",
        "PaleGoldenRod",
        "LightCoral",
        "Khaki",
        "AliceBlue",
        "HoneyDew",
        "Azure",
        "SandyBrown",
        "Wheat",
        "Beige",
        "WhiteSmoke",
        "MintCream",
        "GhostWhite",
        "Salmon",
        "AntiqueWhite",
        "Linen",
        "LightGoldenRodYellow",
        "OldLace",
        "Red",
        "Fuchsia",
        "Magenta",
        "DeepPink",
        "OrangeRed",
        "Tomato",
        "HotPink",
        "Coral",
        "DarkOrange",
        "LightSalmon",
        "Orange",
        "LightPink",
        "Pink",
        "Gold",
        "PeachPuff",
        "NavajoWhite",
        "Moccasin",
        "Bisque",
        "MistyRose",
        "BlanchedAlmond",
        "PapayaWhip",
        "LavenderBlush",
        "SeaShell",
        "Cornsilk",
        "LemonChiffon",
        "FloralWhite",
        "Snow",
        "Yellow",
        "LightYellow",
        "Ivory",
        "Black",
    ]

    def parse_reply_info(replied):
        if not replied:
            return {}
        name = "Unknown"
        emoji_status = None
        chat_id = None

        if replied.from_user:
            chat_id = replied.from_user.id
            name = replied.from_user.first_name
            if replied.from_user.last_name:
                name += f" {replied.from_user.last_name}"
            if getattr(replied.from_user, "emoji_status"):
                emoji_status = str(replied.from_user.emoji_status.custom_emoji_id)

        elif replied.sender_chat:
            chat_id = replied.sender_chat.id
            name = replied.sender_chat.title

        return {
            "chatId": chat_id,
            "entities": Tools.get_msg_entities(replied),
            "name": name,
            "text": replied.text or replied.caption or "",
            "emoji_status": emoji_status,
        }

    async def forward_info(reply):
        if reply.forward_from_chat:
            sid = reply.forward_from_chat.id
            title = reply.forward_from_chat.title
            name = title
        elif reply.forward_from:
            sid = reply.forward_from.id
            try:
                try:
                    name = first_name = reply.forward_from.first_name
                except TypeError:
                    name = "Unknown"
                if reply.forward_from.last_name:
                    last_name = reply.forward_from.last_name
                    name = f"{first_name} {last_name}"
            except AttributeError:
                pass
            title = name
        elif reply.forward_sender_name:
            title = name = sender_name = reply.forward_sender_name
            sid = 0
        elif reply.sender_chat:
            title = name = reply.sender_chat.title
            sid = reply.sender_chat.id
        elif reply.from_user:
            try:
                sid = reply.from_user.id
                try:
                    name = first_name = reply.from_user.first_name
                except TypeError:
                    name = "Unknown"
                if reply.from_user.last_name:
                    last_name = reply.from_user.last_name
                    name = f"{first_name} {last_name}"
            except AttributeError:
                pass
            title = name
        return sid, title, name

    async def t_or_c(message):
        if message.text:
            return message.text
        elif message.caption:
            return message.caption
        else:
            return ""

    async def get_emoji(message):
        if getattr(message.from_user, "emoji_status"):
            emoji_status = str(message.from_user.emoji_status.custom_emoji_id)
        else:
            emoji_status = ""
        return emoji_status

    @staticmethod
    async def quotly(payload: dict) -> bytes:
        # Gunakan sub-endpoint format biner resmi agar server langsung membalas gambar
        url = "https://quote.yuri.ly/quote/generate.png"
        
        # Validasi struktur minimal payload untuk mencegah 'method not found' dari API
        if isinstance(payload, dict) and "messages" in payload:
            # Bersihkan payload dan ambil hanya field utama yang diwajibkan oleh LyoSU/quote-api
            cleaned_messages = []
            for msg in payload["messages"]:
                cleaned_msg = {
                    "from": {
                        "id": msg.get("from", {}).get("id", 1),
                        "name": msg.get("from", {}).get("name", "User")
                    },
                    "text": msg.get("text", "")
                }
                # Jika bot Anda mengirimkan avatar/foto profil, ikut sertakan di bawah
                if "avatar" in msg.get("from", {}):
                    cleaned_msg["from"]["avatar"] = msg["from"]["avatar"]
                if "replyMessage" in msg:
                    cleaned_msg["replyMessage"] = msg["replyMessage"]
                    
                cleaned_messages.append(cleaned_msg)
            
            # Susun ulang payload murni yang dijamin lolos validasi server 400
            payload = {"messages": cleaned_messages}

        async with aiohttp.ClientSession() as session:
            try:
                # Mengirim request menggunakan POST secara eksplisit dengan json body bersih
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        # Langsung kembalikan biner mentah gambar stiker tanpa decode base64
                        return await resp.read()
                    
                    # Penanganan jika terjadi eror dari sisi server API
                    content_type = resp.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        err_json = await resp.json()
                        raise QuotlyException(f"API Error: {err_json.get('error', err_json)}")
                    else:
                        err_text = await resp.text()
                        raise QuotlyException(f"Server Error ({resp.status}): {err_text[:100]}")
                        
            except aiohttp.ClientError as e:
                raise QuotlyException(f"Gagal terhubung ke API Yuri: {str(e)}")


    @staticmethod
    async def make_carbonara(
        code: str, bg_color: str, theme: str, language: str
    ) -> BytesIO:
        url = "https://carbonara.solopov.dev/api/cook"
        json_data = {
            "code": code,
            "paddingVertical": "56px",
            "paddingHorizontal": "56px",
            "backgroundMode": "color",
            "backgroundColor": bg_color,
            "theme": theme,
            "language": language,
            "fontFamily": "Cascadia Code",
            "fontSize": "14px",
            "windowControls": True,
            "widthAdjustment": True,
            "lineNumbers": True,
            "firstLineNumber": 1,
            "name": f"{BOT_NAME}-Carbon",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data) as resp:
                return BytesIO(await resp.read())

    @staticmethod
    async def get_message_content(message):
        if message.text:
            return message.text, "text"
        elif message.document:
            doc = await message.download()
            async with aiofiles.open(doc, mode="r") as f:
                content = await f.read()
            os.remove(doc)
            return content, "document"
        return None, None
