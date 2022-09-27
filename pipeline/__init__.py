import os
import logging
from rich.logging import RichHandler
from pythonjsonlogger import jsonlogger
from .utils.discord_handler import DiscordHandler

fargate = os.getenv('AWS_ECS_FARGATE')

discord_webhook = os.environ['ALERT_WEBHOOK']

format = logging.Formatter('%(levelname)s | %(name)s | %(message)s')

discord_handler = DiscordHandler(discord_webhook, 'notes-pipeline-alert-agent')
discord_handler.setFormatter(format)
discord_handler.setLevel(logging.INFO)

json_handler = logging.StreamHandler()
json_formatter = jsonlogger.JsonFormatter()
json_handler.setFormatter(json_formatter)

if fargate:
    logging.basicConfig(
        format='%(levelname)s | %(name)s | %(message)s',
        level=logging.INFO,
        handlers=[
            json_handler,
            discord_handler],
    )
else:
    logging.basicConfig(
        format='%(levelname)s | %(name)s | %(message)s',
        level=logging.INFO,
        handlers=[
            RichHandler(rich_tracebacks=True),
            discord_handler],
    )
