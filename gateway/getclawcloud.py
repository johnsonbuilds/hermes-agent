import logging
import os

import aiohttp

logger = logging.getLogger(__name__)


async def notify_gateway_ready() -> None:
    """Send a GET request to AGENT_GATEWAY_READY_NOTIFY_URL if set."""
    url = os.getenv("AGENT_GATEWAY_READY_NOTIFY_URL")
    if not url:
        return

    logger.info("Notifying gateway ready: %s", url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status >= 400:
                    logger.warning(
                        "Gateway ready notification failed with status %d: %s",
                        response.status,
                        url,
                    )
                else:
                    logger.info("Gateway ready notification sent successfully")
    except Exception as e:
        logger.warning("Failed to send gateway ready notification to %s: %s", url, e)
