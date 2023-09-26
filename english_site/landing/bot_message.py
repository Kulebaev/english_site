import telebot

TOKEN = '6462231426:AAEpuem2I47PWND6hEgixot7Om984wcAGrM'

bot = telebot.TeleBot(TOKEN)


def start_bot():
    bot.polling()