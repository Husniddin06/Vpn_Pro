from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TARIFFS

def tariffs_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for key, tariff in TARIFFS.items():
        kb.inline_keyboard.append(
            [InlineKeyboardButton(text=f"{tariff['name']} — {tariff['price']} ₽", callback_data=f"tariff_{key}")]
        )
    return kb

def payment_methods_keyboard(tariff_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 СБП", callback_data=f"sbp_{tariff_id}")],
        [InlineKeyboardButton(text="💎 TON", callback_data=f"ton_{tariff_id}")],
        [InlineKeyboardButton(text="💎 USDT", callback_data=f"usdt_{tariff_id}")]
    ])
