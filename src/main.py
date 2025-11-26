import telebot
import logging
import json
from datetime import datetime
import random
import os
from dotenv import load_dotenv

def random_choise_mukin():
    choise = random.randint(1, 5)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    path = os.path.join(images_dir, f"{choise}.jpg")
    return path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Bot")
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "logs/user_data.json"

try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        user_data = json.load(f)
except:
    user_data = {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

def init_user(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            "clicks": 0,
            "cases": 10,
            "total_opens": 0,
            "last_active": datetime.now().isoformat()
        }
        save_data()

def main_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🎯 Клик", "📦 Открыть кейс")
    keyboard.add("📊 Статистика")
    return keyboard

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    init_user(user_id)

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать!\n\nУ вас 10 бесплатных кейсов!\n\nНажмите на кнопки ниже:",
        reply_markup=main_keyboard()
    )
    photo_path = random_choise_mukin()
    bot.send_photo(message.chat.id, open(photo_path, 'rb'))

@bot.message_handler(func=lambda message: message.text == "🎯 Клик")
def click(message):
    user_id = message.from_user.id
    init_user(user_id)

    user_data[str(user_id)]["clicks"] += 1
    user_data[str(user_id)]["last_active"] = datetime.now().isoformat()
    save_data()

    bot.send_message(
        message.chat.id,
        "✅ ⬇️Вы Мушин Артем!⬇️ Всего Мукашечарок: " + str(user_data[str(user_id)]['clicks'])
    )
    photo_path = random_choise_mukin()
    bot.send_photo(message.chat.id, open(photo_path, 'rb'))

@bot.message_handler(func=lambda message: message.text == "📦 Открыть жопу Мушкарева Артема")
def open_case(message):
    user_id = message.from_user.id
    init_user(user_id)

    if user_data[str(user_id)]["cases"] <= 0:
        bot.send_message(message.chat.id, "❌ у вас недостаточно Мушаковых Артемов!")
        return

    rewards = [
        ("💎 Маленький  Мукашевич Артем 11Ж", 5),
        ("💰 Мукашев Артем 11Ж Мукашовский Артем 11Ж", 15),
        ("🏆 Большой Мукин Артем  11Ж", 50)
    ]
    reward_name, reward_value = random.choice(rewards)

    user_data[str(user_id)]["cases"] -= 1
    user_data[str(user_id)]["total_opens"] += 1
    user_data[str(user_id)]["clicks"] += reward_value
    user_data[str(user_id)]["last_active"] = datetime.now().isoformat()
    save_data()

    bot.send_message(
        message.chat.id,
        "🎉 Вы открыли жопу Мушкарева!\n\nНаграда: " + reward_name + " (+" + str(reward_value) + " кликов)\nМукашев Артем 11Ж " + str(user_data[str(user_id)]['cases'])
    )

@bot.message_handler(func=lambda message: message.text == "📊 Статистика")
def stats(message):
    user_id = message.from_user.id
    init_user(user_id)

    stats_text = (
        "📊 Ваша статистика:\n\n" +
        "🎯 Мукашев Артем 11Ж " + str(user_data[str(user_id)]['clicks']) + "\n" +
        "📦 Мукашев Артем 11Ж " + str(user_data[str(user_id)]['cases']) + "\n" +
        "🏆 Мукашев Артем 11Ж " + str(user_data[str(user_id)]['total_opens'])
    )

    bot.send_message(message.chat.id, stats_text)

@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.send_message(message.chat.id, "Мукашев Артем 11Ж", reply_markup=main_keyboard())

if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling(none_stop=True)