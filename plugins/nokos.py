"""
from helpers import CMD
from command import from (
    restock_nokos_cmd,
    delstock_nokos_cmd,
    getstock_nokos_cmd,
)
from clients import star


@CMD.BOT("restock")
@CMD.OWNER_AND_GC
async def _(client, message):
    return await restock_nokos_cmd(client, message)


@CMD.BOT("delstock")
@CMD.OWNER_AND_GC
async def _(client, message):
    return await delstock_nokos_cmd(client, message)


@CMD.BOT("getstock")
@CMD.OWNER_AND_GC
async def _(client, message):
    return await getstock_nokos_cmd(client, message)
"""