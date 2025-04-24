from flask import Flask, request, jsonify
import telebot
from threading import Thread
import time

app = Flask(__name__)
TOKEN = "7913913549:AAGOwDaQK75XuMymXrwbjQVc6MEXJFVnkKU"
bot = telebot.TeleBot(TOKEN)

# Глобальная переменная для хранения URL туннеля
TUNNEL_URL = None

@app.route('/')
def home():
    return "Dropshipping Bot is ready! Tunnel URL: " + str(TUNNEL_URL)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        json_data = request.get_json()
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
    return jsonify({"status": "ok"})

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🛍️ Добро пожаловать в Dropshipping Bot!\n"
                         "Отправьте /help для списка команд")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Список команд:\n"
                         "/start - Начать работу\n"
                         "/help - Помощь\n"
                         "/items - Показать товары")

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def setup_webhook(tunnel_url):
    global TUNNEL_URL
    TUNNEL_URL = tunnel_url
    webhook_url = f"{tunnel_url}/webhook"
    
    # Несколько попыток установки вебхука
    for _ in range(3):
        try:
            bot.remove_webhook()
            time.sleep(1)
            bot.set_webhook(url=webhook_url)
            print(f"Webhook установлен на {webhook_url}")
            break
        except Exception as e:
            print(f"Ошибка установки вебхука: {e}")
            time.sleep(3)

if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Установите здесь ваш URL от LocalXpose после запуска туннеля
    # Пример: "https://yourname.loclx.io"
    setup_webhook("https://9iealdjuax.loclx.io")  # ← ЗАМЕНИТЕ НА ВАШ URL!
    
    # Оставляем основной поток активным
    while True:
        time.sleep(1)