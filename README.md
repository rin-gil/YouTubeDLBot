# YouTubeDLBot


### 🇺🇸 En:

## Bot to download music from YouTube
The working version is available at [@YT_upl_Bot](https://t.me/YT_upl_Bot)

### 1. Bot creation

* Create a new bot with [@BotFather](https://t.me/BotFather) using the /newbot command
* Enter the name of the bot and a description, optionally you can add an image
* Create two commands /start and /help, the script uses commands "/start 🟢 Старт" и "/help ❔Помощь"

### 2. Token writing

* At [@BotFather](https://t.me/BotFather) get an API token for your bot
* In the **main.py** script folder, create an empty **token.txt** file
* Paste the token from [@BotFather](https://t.me/BotFather) into the **token.txt** file and save it

### 3. Running a script

* The script uses **pyTelegramBotAPI**, **pytube** and **moviepy** packages for its operation
* Set them with a command in the terminal:
* `pip install pyTelegramBotAPI`
`pip install pytube`
`pip install moviepy`

### 4. Limitations
* Bot only downloads music (audio file .mp3)
* Bot does not download playlists and live broadcasts
* Due to limitations in the Telegram API, the bot does not download clips longer than 30 minutes
* The name for the audio file is formed from the title of the YouTube video
* Since the name may contain undesirable characters not supported by the file system, all characters except letters, numbers, spaces and the '-' sign are removed from the name, the length of the name is truncated to 100 characters


### 🇷🇺 Ru:

## Бот для скачивания музыки с YouTube
рабочая версия доступна по ссылке [@YT_upl_Bot](https://t.me/YT_upl_Bot)

### 1. Создание бота

* Создайтe нового бота с помощью [@BotFather](https://t.me/BotFather), используя команду /newbot
* Укажите название бота и описание, по желанию можно добавить изображение
* Создайте две команды /start и /help, в скрипте используются команды "/start 🟢 Старт" и "/help ❔Помощь"

### 2. Запись токена

* В [@BotFather](https://t.me/BotFather) получите API токен для своего бота
* В папке со скриптом **main.py** создайте пустой файл **token.txt**
* Вставьте токен из [@BotFather](https://t.me/BotFather) в файл **token.txt** и сохраните его

### 3. Запуск скрипта

* Для своей работы скрипт использует пакеты **pyTelegramBotAPI**, **pytube** и **moviepy**
* Установите их командой в терминале:
* `pip install pyTelegramBotAPI`
`pip install pytube`
`pip install moviepy`

### 4. Ограничения
* Бот скачивает только музыку (аудиофайл .mp3)
* Бот не скачивает плейлисты и живые транляции
* Из-за ограничений в API самого Telegram бот не скачивает клипы продолжительностью больше 30 минут
* Название для аудиофайла формируется из названия видео на YouTube
* Поскольку в названии могут содержаться нежелательные символы, не поддерживаемые файловой системой, из названия убираются все символы, кроме букв, цифр, пробелов и знака '-', длина названия обрезается до 100 символов
