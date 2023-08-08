import logging
import time
from textwrap import dedent
import requests
import environs
import telegram


LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'
logger = logging.getLogger('telegram_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_notification(bot, chat_id, devman_token, long_polling_url=LONG_POLLING_URL):
    timestamp = ''
    while True:
        try:
            response = requests.get(
                long_polling_url,
                headers={'Authorization': devman_token},
                timeout=120,
                params={'timestamp': timestamp}
            )
            response.raise_for_status()
            user_reviews = response.json()
            if 'timestamp_to_request' in user_reviews:
                timestamp = user_reviews['timestamp_to_request']
            else:
                timestamp = ''
                new_attempts = user_reviews['new_attempts']
                for attempt in new_attempts:
                    if attempt['is_negative']:
                        text = f"""\
                        У вас проверили работу: «{attempt['lesson_title']}»
                        К сожалению, в работе нашлись ошибки»
                        Ссылка на урок: {attempt['lesson_url']}
                        """
                    else:
                        text = f"""\
                        У вас проверили работу: «{attempt['lesson_title']}»
                        Преподавателю все понравилось, можно приступать к следующему уроку
                        """
                    bot.send_message(chat_id=chat_id, text=dedent(text))
        except requests.exceptions.ReadTimeout as error:
            logging.error(error)
        except requests.exceptions.ConnectionError as error:
            logging.error(error)
            print('Trying to reconnect over 30 seconds...')
            time.sleep(30)
        except Exception as err:
            logger.exception(err)
            time.sleep(30)


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    chat_id = env('CHAT_ID')
    notification_bot_token = env('TG_TOKEN')
    log_bot_token = env('TELEGRAM_LOG_BOT_TOKEN')
    devman_token = env('DEV_TOKEN')

    logging.basicConfig(level=logging.DEBUG)
    log_bot = telegram.Bot(token=log_bot_token)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    notification_bot = telegram.Bot(token=notification_bot_token)
    send_notification(notification_bot, chat_id, devman_token)
