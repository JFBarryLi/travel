import os
import logging
from rich.logging import RichHandler
from pythonjsonlogger import jsonlogger
from .utils.discord_handler import DiscordHandler

fargate = os.getenv('ECS_CONTAINER_METADATA_URI_V4')

discord_webhook = os.environ['ALERT_WEBHOOK']

format = '%(levelname)s | %(name)s | %(message)s | %(lineno)d'

logging_formatter = logging.Formatter(format)

discord_handler = DiscordHandler(discord_webhook, 'notes-pipeline-alert-agent')
discord_handler.setFormatter(logging_formatter)
discord_handler.setLevel(logging.INFO)

json_handler = logging.StreamHandler()
json_formatter = jsonlogger.JsonFormatter(format)
json_handler.setFormatter(json_formatter)

if fargate:
    logging.basicConfig(
        format=format,
        level=logging.INFO,
        handlers=[
            json_handler,
            discord_handler],
    )
else:
    logging.basicConfig(
        format=format,
        level=logging.INFO,
        handlers=[
            RichHandler(rich_tracebacks=True),
            discord_handler],
    )
