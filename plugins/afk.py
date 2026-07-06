from clients import star
from helpers import CMD
from helpers import AFK_, CMD, Emoji

__MODULES__ = "Afk"
__HELP__ = """<blockquote>Command Help **AFK**</blockquote>

<blockquote>**Enabe afk mode**</blockquote>
    **You can set status to AFK mode**
        `{0}afk` (reason)
    
<blockquote>**Disable afk mode**</blockquote>
    **After AFK mode on, you can set to UNAFK mode**
        `{0}unafk`

<b>   {1}</b>
"""


@CMD.NO_CMD("REP_BLOCK", star)
async def _(client, message):
    em = Emoji(client)
    await em.get()
    return await message.reply_text(
        f"{em.block}**Ga usah reply apalagi tag gw, lu udah block gua anak KONTOL!!**"
    )


@CMD.UBOT("afk")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    rep = message.reply_to_message
    if not rep:
        return await message.reply(f"{emo.gagal}<b>Please reply to message!!</b>")
    return await AFK_.set_afk(client, message, emo)


@CMD.NO_CMD("AFK", star)
@CMD.capture_err
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    return await AFK_.get_afk(client, message, emo)


@CMD.UBOT("unafk")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    return await AFK_.unset_afk(client, message, emo)
