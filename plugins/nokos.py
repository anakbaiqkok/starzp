



@CMD.BOT("restock")
async def _(client, message):
    return await restock_nokos_cmd(client, message)


@CMD.BOT("delstock")
async def _(client, message):
    return await delstock_nokos_cmd(client, message)


@CMD.BOT("getstock")
async def _(client, message):
    return await getstock_nokos_cmd(client, message)