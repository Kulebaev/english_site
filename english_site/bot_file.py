import os
from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "english_site.settings")  # Замените "your_project" на имя вашего Django проекта.
setup()


import telebot
from django.core.files import File
from landing.models import Book, Image
from io import BytesIO

TOKEN = '6415362149:AAHokYJZXCwMTLNUAyr-rxqOJIdSu4OM6p0'

bot = telebot.TeleBot(TOKEN)

# Словарь для отслеживания соответствия между ID чата и ID книги
chat_book_ids = {}
# Словарь для отслеживания типа файла, который ожидается
chat_file_types = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id

    # Просим пользователя отправить наименование книги
    bot.send_message(chat_id, "Пожалуйста, отправьте наименование книги.")

@bot.message_handler(func=lambda message: True 
                     and not message.text.lower() == '/exit' 
                     and not message.text.lower() == '/start')
def receive_title(message):
    chat_id = message.chat.id

    # Извлекаем наименование книги из сообщения
    title = message.text

    # Создаем запись в базе данных
    book_entry = Book(title=title)
    book_entry.save()

    # Сохраняем соответствие между ID чата и ID книги
    chat_book_ids[chat_id] = book_entry.id

    # Просим пользователя отправить файл книги
    bot.send_message(chat_id, "Теперь отправьте файл книги.")

    # Устанавливаем ожидание файла книги
    chat_file_types[chat_id] = "book"

@bot.message_handler(content_types=['document', 'photo'])
def receive_files(message):
    print(chat_book_ids, chat_file_types)
    chat_id = message.chat.id

    if chat_id not in chat_file_types:
        bot.send_message(chat_id, 'Неожиданное сообщение. Пожалуйста, начните снова с команды /start.')
        return

    if message.document:
        file_info = bot.get_file(message.document.file_id)
        file = bot.download_file(file_info.file_path)
        name = message.document.file_name
    elif message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
        file = bot.download_file(file_info.file_path)
        print(file_info)
        name = 'image.jpg' # Имя по умолчанию для фотографии

    # Получаем ID книги из chat_book_ids
    book_id = chat_book_ids.get(chat_id)

    if book_id is not None:
        # Сохраняем файл и изображение в записи по ID
        with BytesIO(file) as file_buffer:
            book_entry = Book.objects.get(id=book_id)
            if chat_file_types[chat_id] == "book":
                book_entry.file.save(name, File(file_buffer))
                # Просим пользователя отправить изображение
                bot.send_message(chat_id, "Теперь отправьте изображение(или несколько) для этой книги.")
                # Устанавливаем ожидание изображения
                chat_file_types[chat_id] = "image"
            elif chat_file_types[chat_id] == "image":
                # Сохраняем изображение в модель Image
                image = Image()
                image.file.save(name, File(file_buffer))
                image.save()

                # Добавляем изображение к списку изображений книги
                book_entry.image.add(image)
                # Отправляем сообщение о сохранении файла и ID книги

                bot.send_message(chat_id, f'Файл "{name}" сохранен в базе данных. ID книги: {book_id}'
                                 f'\nВы можете добавить файлы к этой книге. Напишите /exit если хотите выйти из этой книги.')
        return

    bot.send_message(chat_id, 'Не найдена связь с книгой. Пожалуйста, начните снова с команды /start.')


@bot.message_handler(commands=['exit'])
def start(message):

    chat_id = message.chat.id

    # Проверяем наличие ключа чата в словаре chat_book_ids
    if chat_id in chat_book_ids:
        # Удаляем соответствие между ID чата и ID книги
        del chat_book_ids[chat_id]

    # Проверяем наличие ключа чата в словаре chat_file_types
    if chat_id in chat_file_types:
        # Удаляем соответствие между ID чата и типом файла
        del chat_file_types[chat_id]

    bot.send_message(chat_id, "Вы можете добавить новую книгу. Напишите наименование книги.")

bot.polling(none_stop=True)