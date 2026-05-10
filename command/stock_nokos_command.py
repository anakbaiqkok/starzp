import traceback

from database import db
from config import OWNER_ID
from logs import logger


async def restock_nokos_cmd(client, message):
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        return await message.reply("<b>❌ Khusus owner.</b>")

    try:
        args = message.text.split(maxsplit=1)

        if len(args) < 2:
            return await message.reply(
                """
<b>Format salah.</b>

Gunakan:
<code>.restock id|harga|nomor|otp|2fa|session</code>

Contoh:
<code>.restock 123456|15000|628xxxx|12345|password2fa|SESSION_STRING</code>

Kalau tidak ada 2FA:
<code>.restock 123456|15000|628xxxx|12345|-|SESSION_STRING</code>
"""
            )

        data = args[1].split("|")

        if len(data) < 6:
            return await message.reply(
                "<b>❌ Data kurang. Format harus:</b>\n"
                "<code>.restock id|harga|nomor|otp|2fa|session</code>"
            )

        nokos_id = int(data[0].strip())
        price = data[1].strip()
        phone = data[2].strip()
        otp = data[3].strip()
        twofa = data[4].strip()
        session = "|".join(data[5:]).strip()

        if twofa == "-":
            twofa = None

        await db.add_nokos(
            _id=nokos_id,
            price=price,
            session=session,
            phone=phone,
            otp=otp,
            twofa=twofa,
        )

        return await message.reply(
            f"""
<b>✅ Stok berhasil ditambahkan.</b>

<blockquote>
🆔 ID: <code>{nokos_id}</code>
📱 Nomor: <code>{phone}</code>
🔐 OTP: <code>{otp}</code>
🔒 2FA: <code>{twofa or '-'}</code>
💵 Harga: <code>{price}</code>
</blockquote>
"""
        )

    except Exception:
        logger.error(f"RESTOCK NOKOS ERROR: {traceback.format_exc()}")
        return await message.reply("<b>❌ Gagal menambahkan stok.</b>")


async def delstock_nokos_cmd(client, message):
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        return await message.reply("<b>❌ Khusus owner.</b>")

    try:
        args = message.text.split(maxsplit=1)

        if len(args) < 2:
            return await message.reply(
                "<b>Format:</b>\n<code>.delstock id</code>"
            )

        nokos_id = int(args[1].strip())

        data = await db.get_nokos_by_id(nokos_id)
        if not data:
            return await message.reply("<b>❌ Stok tidak ditemukan.</b>")

        await db.delete_nokos(nokos_id)

        return await message.reply(
            f"<b>✅ Stok berhasil dihapus.</b>\n\n🆔 ID: <code>{nokos_id}</code>"
        )

    except Exception:
        logger.error(f"DELETE STOCK NOKOS ERROR: {traceback.format_exc()}")
        return await message.reply("<b>❌ Gagal menghapus stok.</b>")


async def getstock_nokos_cmd(client, message):
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        return await message.reply("<b>❌ Khusus owner.</b>")

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