import os
import logging
from rich.logging import RichHandler
from .utils.discord_handler import DiscordHandler

discord_webhook = os.environ['ALERT_WEBHOOK']

format = logging.Formatter('%(levelname)s | %(name)s | %(message)s')

discord_handler = DiscordHandler(discord_webhook, 'notes-pipeline-alert-agent')
discord_handler.setFormatter(format)
discord_handler.setLevel(logging.INFO)

logging.basicConfig(
    format='%(levelname)s | %(name)s | %(message)s',
    level=logging.INFO,
    handlers=[
        RichHandler(rich_tracebacks=True),
        discord_handler],
)
