from helpers import CMD
from command import from (
    restock_nokos_cmd,
    delstock_nokos_cmd,
    getstock_nokos_cmd,
)



@CMD.BOT("restock")
async def _(client, message):
    return await restock_nokos_cmd(client, message)


@CMD.BOT("delstock")
async def _(client, message):
    return await delstock_nokos_cmd(client, message)


@CMD.BOT("getstock")
async def _(client, message):
    return await getstock_nokos_cmd(client, message)