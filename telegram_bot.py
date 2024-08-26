import telebot
import logging
import threading
import time

from parsing.NextSatSun import NextSatSun
from parsing.catch_data import catch_data




# Включаем логирование
logging.basicConfig(level=logging.DEBUG)

# Замените 'YOUR_TOKEN' на токен вашего бота
TOKEN = 'HAHA NO'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения сообщений пользователей
user_messages = {}

# Время в секундах между отправками сообщений
MESSAGE_INTERVAL = 10  # Измените на нужный интервал

def send_periodic_message(user_id):
    """Функция для отправки периодического сообщения пользователю."""
    logging.info(f"Periodic message thread started for user {user_id}")
    while True:
        time.sleep(MESSAGE_INTERVAL)
        try:
            catch_data_tool = catch_data(url='https://www.aviasales.ru/?params=LED3108KGD01091')
            price = catch_data_tool.proceed()

            bot.send_message(user_id, str(price))
            logging.info(f"Periodic message sent to user {user_id}")
        except Exception as e:
            logging.error(f"Error sending periodic message to user {user_id}: {e}")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    # Получаем ID пользователя
    user_id = message.chat.id

    # Получаем текст сообщения
    user_message = message.text

    # Сохраняем сообщение для пользователя
    if user_id in user_messages:
        user_messages[user_id].append(user_message)
    else:
        user_messages[user_id] = [user_message]

    bot.reply_to(message, 'Я только высылаю сообщение')

    # Сохраняем сообщения в файл
    with open("messages.txt", "a") as f:
        f.write(f"User {user_id}: {user_message}\n")

    # Запускаем поток для периодической отправки сообщений, если он еще не запущен
    if not any(t.name == f"PeriodicMessageThread-{user_id}" for t in threading.enumerate()):
        thread = threading.Thread(target=send_periodic_message, args=(user_id,), name=f"PeriodicMessageThread-{user_id}")
        thread.daemon = True  # Позволяет завершить поток при завершении основного потока
        thread.start()
        logging.info(f"Periodic message thread started for user {user_id}")

# Запускаем бота
if __name__ == '__main__':
    try:
        logging.info("Starting bot...")
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Error running bot: {e}")