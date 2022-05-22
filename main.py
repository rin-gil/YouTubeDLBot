# Importing the pyTelegramBotAPI package for Telegram API
# install the package with the command "pip install pyTelegramBotAPI"
import telebot
from telebot import types
# Import the pytube package for searching and downloading videos from YouTube
# Install the package with the command "pip install pytube"
from pytube import YouTube
from pytube import Search
# Import the package moviepy convert the downloaded video into an audio file .mp3
# install the package with the command "pip install moviepy"
import moviepy.editor as mp
# Import the built-in os module for working with files
import os
# Import the built-in time conversion module time output from seconds to hours:minutes:seconds
import time


# Read the bot's token from the token.txt file
def get_token():
    with open('token.txt') as file:
        return file.read()


bot = telebot.TeleBot(get_token())


# Removes unwanted characters from the video title or user input and reduces it to 100 characters
def correct_name(name):
    string = name[:100]
    result = []
    for char in string:
        if char.isalnum():
            result.append(char)
        elif char.isspace() and (not result or not result[-1].isspace()):
            result.append(char)
        elif char == '-':
            result.append(char)
    return "".join(map(str, result))


# Converts mp4 video file to mp3 audio file
def converttomp3(mp4_file, mp3_file):
    clip = mp.AudioFileClip(mp4_file)
    clip.write_audiofile(mp3_file)
    clip.close()
    os.remove(mp4_file)


# Downloads videos and converts them to mp3
def download(url):
    try:
        audio_obj = YouTube(url)
        # Due to limitations of the Telegram API, the bot does not download videos longer than 30 minutes
        if audio_obj.length <= 1800:
            folder = './downloads'
            stream = audio_obj.streams.get_audio_only()
            video_file = correct_name(audio_obj.title)
            stream.download(folder, filename=video_file + '.mp4')
            mp4_file = folder + '/' + video_file + '.mp4'
            mp3_file = folder + '/' + video_file + '.mp3'
            converttomp3(mp4_file, mp3_file)
            return mp3_file
        else:
            return 'too_long'
    except Exception as ex:
        print(ex)
        return 'error'


# Checks if the user's input is a link to a YouTube video
def is_youtube_url(url):
    if url.startswith('https://youtube.com/watch') is True\
            or url.startswith('https://www.youtube.com/watch') is True\
            or url.startswith('https://youtu.be/') is True\
            or url.startswith('https://youtube.com/playlist') is True:
        # To save space and traffic on the server, the bot does not download playlists
        if url.find('list') != -1:
            return 'playlist'
        return True
    else:
        return False


# Search for the query entered by the user on YouTube,
# display the first 3 results, skip the video longer than 30 minutes
def search_result(query):
    result = []
    count_query = 0
    result_count = 0
    try:
        search_query = Search(query)
        while result_count < 3:
            length = search_query.results[count_query].length
            if length <= 1800:
                link = search_query.results[count_query].watch_url
                title = search_query.results[count_query].title
                duration = time.strftime("%H:%M:%S", time.gmtime(length))
                card = f'<a href="{link}"><b>{title}</b></a>\n<b>Время:  {duration}</b>'
                result.append([card, link])
                result_count += 1
                count_query += 1
            else:
                count_query += 1
        return result
    except Exception as ex:
        print(ex)
        return False


# Handle clicking on the Download button in the search results
@bot.callback_query_handler(func=lambda call: True)
def search_answer(call):
    if call.data == 'download':
        bot.send_message(call.message.chat.id, '⏬ Качаю..')
        bot.answer_callback_query(callback_query_id=call.id)
        url = call.message.entities[0].url
        file = download(url)
        audio = open(file, 'rb')
        try:
            bot.send_audio(call.message.chat.id, audio)
        except Exception as ex:
            print(ex)
            bot.send_message(call.message.chat.id, '❌ Ошибка при отправке файла!\n\n'
                                                   'Попробуй скачать что-то другое. 🙁')
        finally:
            audio.close()
            os.remove(file)


# Create control buttons in the bot and display a message if a user sends a /start or /help command
@bot.message_handler(commands=['start', 'help'])
def handle_commands(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_command = types.KeyboardButton('🟢 Старт')
    help_command = types.KeyboardButton('❔Помощь')
    markup.add(start_command, help_command)
    if message.text == '/start':
        bot.send_message(message.chat.id,
                         'Напиши мне <b>название песни</b> или сбрось <b>ссылку</b> на видеоролик. 😉',
                         parse_mode='html', reply_markup=markup)
    elif message.text == '/help':
        bot.send_message(message.chat.id,
                         'Я умею скачивать песни с YouTube!\n\n'
                         'Напиши мне <b>название песни</b>, '
                         'или сбрось <b>ссылку</b> на видеоролик.',
                         parse_mode='html', reply_markup=markup)


# If the user has sent anything but a message
@bot.message_handler(func=lambda message: True, content_types=['audio',
                                                               'document',
                                                               'photo',
                                                               'sticker',
                                                               'video',
                                                               'video_note',
                                                               'voice',
                                                               'location',
                                                               'contact',
                                                               'poll',
                                                               'game',
                                                               'animation',
                                                               'pinned_message'])
def unknown_message(message):
    bot.reply_to(message, "🤷 Я не знаю, что с этим делать.\n\n"
                          'Напиши мне <b>название песни</b>, '
                          'или сбрось <b>ссылку</b> на видеоролик.',
                 parse_mode='html')


# Handles input text messages from the user
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.chat.type == 'private':
        # If the user presses the Start button and the Help button, the following messages are displayed
        if message.text == '🟢 Старт':
            bot.send_message(message.chat.id,
                             'Напиши мне <b>название песни</b> или сбрось <b>ссылку</b> на видеоролик. 😉',
                             parse_mode='html')
        elif message.text == '❔Помощь':
            bot.send_message(message.chat.id,
                             'Я умею скачивать песни с YouTube!\n\n'
                             'Напиши мне <b>название песни</b>, '
                             'или сбрось <b>ссылку</b> на видеоролик.',
                             parse_mode='html')
        else:
            # If a user sent a link to a playlist from YouTube
            if is_youtube_url(message.text) == 'playlist':
                bot.send_message(message.chat.id, '❌ Я не могу скачивать плейлисты!')
            # If a user sent a link to a YouTube video
            elif is_youtube_url(message.text) is True:
                bot.send_message(message.chat.id, '⏬ Качаю..')
                file = download(message.text)
                # If the video is too long
                if file == 'too_long':
                    bot.send_message(message.chat.id, '❌ Упс..\n\n'
                                                      'Этот ролик длится больше 30 минут!\n'
                                                      'Найди что-нибудь покороче. 😒')
                # If an error occurs when downloading a video (for example, a restricted video)
                elif file == 'error':
                    bot.send_message(message.chat.id, '❌ Ошибка при скачивании!\n\n'
                                                      'Кажется, я не смогу это скачать. 🙁')
                # If the video downloaded and converted, send the file to the user
                else:
                    audio = open(file, 'rb')
                    try:
                        bot.send_audio(message.chat.id, audio)
                    except Exception as ex:
                        print(ex)
                        bot.send_message(message.chat.id, '❌ Ошибка при отправке файла!\n\n'
                                                          'Попробуй скачать что-то другое. 🙁')
                    finally:
                        audio.close()
                        os.remove(file)
            # If the user sent a message that is not a YouTube link
            elif is_youtube_url(message.text) is False:
                if message.text.startswith('https://') is True or message.text.startswith('http://') is True:
                    bot.send_message(message.chat.id, '❌ Это не похоже на ссылку с YouTube!')
                # Trying to find what the user sent in
                else:
                    bot.send_message(message.chat.id, '🔍 Ищу..')
                    search_on_youtube = search_result(correct_name(message.text))
                    # If there is an error during the search
                    if search_on_youtube is False:
                        bot.send_message(message.chat.id, '❌ Упс..\n\n'
                                                          'Я не могу это найти.\n'
                                                          'Попробуй поискать что-то другое. 😒')
                    # Showing the first 3 search results
                    else:
                        markup_inline = types.InlineKeyboardMarkup()
                        download_button = types.InlineKeyboardButton(text='⏬ Скачать', callback_data='download')
                        markup_inline.add(download_button)
                        bot.send_message(message.chat.id, '👇 Смотри, что я нашел:')
                        for count in range(3):
                            bot.send_message(message.chat.id, search_on_youtube[count][0],
                                             reply_markup=markup_inline,
                                             parse_mode='html')


if __name__ == '__main__':
    print('YouTube DL Bot working...')
    bot.polling(none_stop=True)
    print('YouTube DL Bot stopped!')
