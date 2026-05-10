import traceback

from config import SUDO_OWNERS
from database import db
from logs import logger


def sudo_only(message):
    user = message.from_user or message.sender_chat
    return user and user.id in SUDO_OWNERS


async def restock_nokos_cmd(client, message):
    user = message.from_user

    if user.id not in SUDO_OWNERS:
        return await message.reply("<b>Perintah ini khusus SUDO_OWNERS!!</b>")

    if len(message.command) < 3:
        return await message.reply(
            f"<b>{message.text.split()[0]} [user_id/username] [harga]</b>"
        )

    user_id = message.command[1]
    harga = message.command[2]

    try:
        harga = str(harga)
    except Exception:
        return await message.reply("<b>Harga tidak valid!</b>")

    try:
        target = await client.get_users(user_id)
        get_id = target.id
    except Exception as error:
        return await message.reply(str(error))

    cek_nokos = await db.get_nokos_by_id(get_id)
    if cek_nokos:
        return await message.reply(
            f"<b>Pengguna dengan ID:</b> <code>{get_id}</code> "
            f"<b>sudah memiliki akses nokos!</b>"
        )

    await db.add_nokos(
        _id=get_id,
        price=harga,
        session="",
        phone=None,
        otp=None,
        twofa=None,
    )

    await message.reply(
        f"✅ <b>Akses nokos diberikan kepada</b> <code>{get_id}</code>\n"
        f"<b>Harga:</b> <code>{harga}</code>\n\n"
        f"<b>Silahkan pergi ke @{bot.me.username}</b>"
    )

    target1 = (
        f"<a href=tg://user?id={message.from_user.id}>"
        f"{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
    )

    target2 = (
        f"<a href=tg://user?id={target.id}>"
        f"{target.first_name} {target.last_name or ''}</a>"
    )

    try:
        await bot.send_message(
            LOG_SELLER,
            f"<b>User: {target1} gives nokos access to: {target2}</b>\n"
            f"<b>Harga:</b> <code>{harga}</code>",
        )
    except Exception:
        pass

    try:
        return await bot.send_message(
            get_id,
            f"<b>Selamat! Akun anda sudah memiliki akses untuk pembuatan Nokos.</b>\n\n"
            f"<b>Harga:</b> <code>{harga}</code>",
            reply_markup=kb(
                [["✅ Restock Nokos"]],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
    except Exception:
        pass


async def delstock_nokos_cmd(client, message):
    if not sudo_only(message):
        return await message.reply("<b>❌ Perintah ini khusus SUDO OWNERS.</b>")

    try:
        args = message.text.split(maxsplit=1)

        if len(args) < 2:
            return await message.reply(
                "<b>Format:</b>\n<code>/delstock id</code>"
            )

        nokos_id = int(args[1].strip())

        data = await db.get_nokos_by_id(nokos_id)
        if not data:
            return await message.reply("<b>❌ Stok tidak ditemukan.</b>")

        await db.delete_nokos(nokos_id)

        return await message.reply(
            f"<b>✅ Stok berhasil dihapus.</b>\n\n"
            f"🆔 ID: <code>{nokos_id}</code>"
        )

    except Exception:
        logger.error(f"DELETE STOCK NOKOS ERROR: {traceback.format_exc()}")
        return await message.reply("<b>❌ Gagal menghapus stok.</b>")


async def getstock_nokos_cmd(client, message):
    if not sudo_only(message):
        return await message.reply("<b>❌ Perintah ini khusus SUDO OWNERS.</b>")

    try:
        stok = await db.get_nokos()

        if not stok:
            return await message.reply("<b>❌ Stok nokos kosong.</b>")

        text = "<b>📦 List Stok Nokos</b>\n\n"

        for no, data in enumerate(stok, start=1):
            text += f"""
<blockquote>
<b>{no}. Nokos Telegram</b>
🆔 ID: <code>{data.get("_id")}</code>
📱 Nomor: <code>{data.get("phone", "-")}</code>
🔐 OTP: <code>{data.get("otp", "-")}</code>
🔒 2FA: <code>{data.get("twofa") or "-"}</code>
💵 Harga: <code>{data.get("price")}</code>
</blockquote>
"""

        return await message.reply(text)

    except Exception:
        logger.error(f"GET STOCK NOKOS ERROR: {traceback.format_exc()}")
        return await message.reply("<b>❌ Gagal mengambil stok.</b>")