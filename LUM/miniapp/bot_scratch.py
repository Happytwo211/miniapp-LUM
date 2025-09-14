import telebot
from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
import requests

API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
WEBAPP_URL = "https://yourdomain.com/profile/"  # ссылка на Django (добавится user_id)

bot = telebot.TeleBot(API_TOKEN)


# Старт — предлагаем открыть профиль в WebApp
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = KeyboardButton(
        text="👤 Открыть профиль",
        web_app=WebAppInfo(url=f"{WEBAPP_URL}{message.from_user.id}/")
    )
    keyboard.add(webapp_button)

    bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.first_name}! Нажми кнопку ниже, чтобы открыть свой профиль 👇",
                     reply_markup=keyboard)

    # 🔥 Обновляем профиль в Django
    update_profile(message)


def update_profile(message):
    """Отправляем данные в Django, чтобы обновить профиль"""
    payload = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "avatar_url": f"https://t.me/i/userpic/320/{message.from_user.username}.jpg" if message.from_user.username else "",
        "phone_number": ""  # если захочешь — можно запросить у юзера через contact
    }

    try:
        requests.post("https://yourdomain.com/api/update_profile/", json=payload, timeout=5)
    except Exception as e:
        print("Ошибка обновления профиля:", e)


if __name__ == "__main__":
    bot.polling(none_stop=True)
