import asyncio
from logs import logger

# Setup event loop default
try:
    asyncio.set_event_loop(asyncio.new_event_loop())
    logger.info("🚀 Asyncio event loop berhasil disiapkan secara global.")
except Exception as e:
    logger.error(f"❌ Gagal menyiapkan event loop: {e}")

# Import client
from .clients import BaseClient, Bot, UserBot, bot, navy
