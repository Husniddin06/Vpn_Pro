from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Купить VPN")],
            [KeyboardButton(text="💰 Тарифы"), KeyboardButton(text="👥 Рефералы")],
            [KeyboardButton(text="💰 Баланс"), KeyboardButton(text="📤 Вывести деньги")],
            [KeyboardButton(text="📖 Инструкция"), KeyboardButton(text="🆘 Поддержка")]
        ],
        resize_keyboard=True
    )
