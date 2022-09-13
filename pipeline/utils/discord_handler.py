import time
import logging
import requests


class DiscordHandler(logging.Handler):
    def __init__(self, webhook_url, agent):
        logging.Handler.__init__(self)
        self.webhook_url = webhook_url
        self.retry_limit = 3
        self.retry_count = 0
        self.x_ratelimit_remaining = None
        self.x_ratelimit_reset_after = None
        self.headers = {'User-Agent': agent}

    def write_to_discord(self, message):
        if self.x_ratelimit_remaining is None:
            pass
        elif self.x_ratelimit_remaining < 1:
            if self.x_ratelimit_reset_after is not None:
                time.sleep(self.x_ratelimit_reset_after)
            else:
                time.sleep(2)

        request = requests.post(
            self.webhook_url,
            headers=self.headers,
            data={
                'content': message
            }
        )

        self.x_ratelimit_reset_after = int(request.headers['x-ratelimit-reset-after'])
        self.x_ratelimit_remaining = int(request.headers['x-ratelimit-remaining'])

        if request.status_code == 404:
            raise requests.exceptions.InvalidURL(f'Discord Webhook 404: {request.text}')

        if request.status_code == 429:
            if self.retry_count < self.retry_limit:
                if self.x_ratelimit_reset_after is not None:
                    time.sleep(self.x_ratelimit_reset_after)
                else:
                    time.sleep(2)
                self.retry_count += 1
                self.write_to_discord

        if not request.ok:
            raise requests.exceptions.HTTPError(
                f'Discord WebHook returned status code {request.status_code}, {request.text}'
            )

    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelno > 20:
                self.write_to_discord(f'```fix\n{msg}\n```')
            else:
                self.write_to_discord(f'```{msg}```')
        except Exception:
            self.handleError(record)
