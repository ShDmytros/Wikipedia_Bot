from get_info import parsing
from data.my_key import key
import telebot
from telebot import types

# pip install pyTelegramBotAPI


bot = telebot.TeleBot(key)
user_language = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/start")
    item2 = types.KeyboardButton("/ukrainian")
    item3 = types.KeyboardButton("/english")
    markup.add(item1, item2, item3)

    # ukrainian
    bot.send_message(message.chat.id, "Українська мова🇺🇦")
    bot.send_message(message.chat.id, "Це версія 2.0 Вікіпедії бота! Якщо будуть якісь помилки, пишіть @ShDmytros")
    bot.send_message(message.chat.id, "Автор: Дмитро Штучка")
    bot.send_message(message.chat.id,
                     "1.Доступна лише українська мова🇺🇦 та англійська мова🇬🇧, з будь якими іншими мовами бот "
                     "працювати не буде!\n\n2.Пишіть обов'язково коректно.")
    bot.send_message(message.chat.id,
                     'Вкажіть мову спілкування, щоб обрати мову спілкування, напишіть команду, для української '
                     '/ukrainian, та для англійської /english')

    # english
    bot.send_message(message.chat.id, "English language🇬🇧")
    bot.send_message(message.chat.id, "This is a version 2.0 of the bot's Wikipedia! If there are any errors, "
                                      "write to @ShDmytros")
    bot.send_message(message.chat.id, "Author: Dmytro Shtuchka")
    bot.send_message(message.chat.id,
                     "1.Only Ukrainian🇺🇦 and English🇬🇧 are available, with any other languages the bot"
                     "will not work!\n\n2.Be sure to write correctly.")
    bot.send_message(message.chat.id,
                     'Specify the language of communication to select the language of communication, write a command, '
                     'for Ukrainian /ukrainian and for English /english', reply_markup=markup)


@bot.message_handler(commands=['ukrainian'])
def ua(lang):
    user_language[lang.chat.id] = "ua"

    bot.send_message(lang.chat.id,
                     'Ви обрали українську мову🇺🇦, якщо Ви хочете змінити мову, напишіть команду /start та поторіть '
                     'все зпочатку. ')
    bot.send_message(lang.chat.id, 'Тепер напишіть, що Ви хочете знайти, до прикладу "Лос Анджелес", "Наполеонівські війни", '
                                   'Собаки, "Херсон", "Львів" тощо.')


@bot.message_handler(commands=['english'])
def en(lang):
    user_language[lang.chat.id] = "en"

    bot.send_message(lang.chat.id,
                     'You have chosen English language🇬🇧, if you want to change the language, write the command '
                     '/start and start over.')
    bot.send_message(lang.chat.id, 'Now write down what you want to find, for example, "Los Angeles", "Napoleonic Wars", '
                                   '"Dogs", "Kherson", "Lviv", etc.')


@bot.message_handler(content_types=["text"])
def message_handler(message):
    language = user_language.get(message.chat.id)

    if language == "ua":
        bot.send_message(message.chat.id, "Трохи зачекайте, йде пошук інформації.")
        bot.send_message(message.chat.id, "🔎")

        data = parsing(text=message.text, lang="ua")

    elif language == "en":
        bot.send_message(message.chat.id, "Please wait a moment, the bot is searching for information.")
        bot.send_message(message.chat.id, "🔎")

        data = parsing(text=message.text, lang="en")

    else:
        bot.send_message(message.chat.id, "Будь ласка, спочатку оберіть мову командою /start.")
        bot.send_message(message.chat.id, "Please first select the language with the /start command.")
        return

    data_info: str = data.data_list if data and hasattr(data, "data_list") else None
    data_photo: str = data.photo if data and hasattr(data, "photo") else None

    if "None" in data_info:
        bot.send_message(message.chat.id, "Інформацію не знайдено!" if language == "ua" else "Information not found!")
    else:
        bot.send_message(message.chat.id, text=data_info)

        if "None" not in data_photo:
            bot.send_photo(message.chat.id, data_photo)


bot.polling(non_stop=True)
