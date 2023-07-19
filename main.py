import logging
import time
from textwrap import dedent
import requests
import environs
import telegram


LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'


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
            serialized_response = response.json()
            if 'timestamp_to_request' in serialized_response:
                timestamp = serialized_response['timestamp_to_request']
            else:
                timestamp = ''
                new_attempts = serialized_response['new_attempts']
                for attempt in new_attempts:
                    if attempt['is_negative']:
                        text = f"""У вас проверили работу: «{attempt['lesson_title']}»\n
                               К сожалению, в работе нашлись ошибки»\nСсылка на урок: {attempt['lesson_url']}"""
                    else:
                        text = f"""У вас проверили работу: «{attempt['lesson_title']}»\n
                               Преподавателю все понравилось, можно приступать к следующему уроку"""
                    bot.send_message(chat_id=chat_id, text=dedent(text))
        except requests.exceptions.ReadTimeout as error:
            logging.debug(error)
        except requests.exceptions.ConnectionError as error:
            logging.debug(error)
            print('Trying to reconnect over 30 seconds...')
            time.sleep(30)


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()
    chat_id = env('CHAT_ID')
    telegram_token = env('TG_TOKEN')
    devman_token = env('DEV_TOKEN')
    bot = telegram.Bot(token=telegram_token)

    send_notification(bot, chat_id, devman_token)
