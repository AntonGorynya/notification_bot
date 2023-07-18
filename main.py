import logging
import time
import requests
import environs
from telegram.ext import Updater, ConversationHandler, CommandHandler


URL = 'https://dvmn.org/api/user_reviews/'
LONG_POLLING_URL = 'https://dvmn.org/api/long_polling/'


def start(update, _):
    username = update.message.chat['username']
    update.message.reply_text(f'Привет {username}!')
    send_notification(update)


def cancel(update, _):
    update.message.reply_text(
        'До новых встреч!',
    )
    return ConversationHandler.END


def send_notification(update):
    timestamp = ''
    while True:
        try:
            response = requests.get(
                LONG_POLLING_URL,
                headers=headers,
                timeout=120,
                params={'timestamp': timestamp}
            )
            response.raise_for_status()
            if 'timestamp_to_request' in response.json():
                timestamp = response.json()['timestamp_to_request']
            else:
                timestamp = ''
                response = response.json()
                new_attempts = response['new_attempts']
                for attempt in new_attempts:
                    if attempt['is_negative']:
                        text = f"У вас проверили работу: «{attempt['lesson_title']}»\n" \
                               f"К сожалению, в работе нашлись ошибки»\nСсылка на урок: {attempt['lesson_url']}"
                    else:
                        text = f"У вас проверили работу: «{attempt['lesson_title']}»\n" \
                               f"Преподавателю все понравилось, можно приступать к следующему уроку"
                    update.message.reply_text(text)
        except requests.exceptions.ReadTimeout as error:
            logging.debug(error)
        except requests.exceptions.ConnectionError as error:
            logging.debug(error)
            print('Trying to reconnect over 30 seconds...')
            time.sleep(30)


if __name__ == '__main__':
    env = environs.Env()
    env.read_env()

    telegram_token = env('TG_TOKEN')
    headers = {
        'Authorization': env('DEV_TOKEN')
    }

    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(CommandHandler('start', start, run_async=True))
    updater.start_polling()
    updater.idle()
