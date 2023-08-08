# Notification Bot
Данный репозиторий представляет собой бота, позволяющего получать уведомление о проверенных работах с сайта https://dvmn.org.

### Как установить
Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```

Перед запуском создайте файл **.env** вида:
```properties
DEV_TOKEN='Token хххх'
TG_TOKEN='хххх:уууу'
CHAT_ID='ID вашего чата'
TELEGRAM_LOG_BOT_TOKEN='Токен от лог бота хххх:yyyy'
```
Где `DEV_TOKEN` - токен с сайта  https://dvmn.org, а `TG_TOKEN` - токен телеграм бота.

- Токен для Телеграм бота вы можете получить https://telegram.me/BotFather
- Токен для подключения к vmn.org вы можете получить https://dvmn.org/api/docs/
- Для получения CHAT_ID напишите любое сообщение вашему боту, после чего перейдите по ссылке https://api.telegram.org/bot{TG_TOKEN}/getUpdates 

### Как запустить
Для запуска бота спикера используйте команду
```sh
python main.py 
```
