from api_token import API_TOKEN_BOT
from app import convert,log_request
from telebot import TeleBot


bot = TeleBot(API_TOKEN_BOT)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    answer = convert(message.text)
    print(message.chat.id, message.text, answer, sep=' -- ')
    log_request(message.chat.id, message.text, answer)
    bot.send_message(message.chat.id, str(answer))



bot.infinity_polling()