from get_info import parsing
from my_key import key
import telebot

# pip install pyTelegramBotAPI


bot = telebot.TeleBot(key)


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Це альфа версія Вікіпедії бота!")
    bot.send_message(message.chat.id, "1.Доступна лише українська мова🇺🇦, з будь якими іншими мовами бот працювати не буде!\n2.Пишіть обов'язково коректно.")

@bot.message_handler()
def main(message):
    data = parsing(text=message.text)
    data_info = str(data.data_list)
    if "None" in data_info:
        bot.send_message(message.chat.id, "Інформацію не знайдено!")
    else:
        bot.send_message(message.chat.id, text=data_info)

bot.polling(non_stop=True)


