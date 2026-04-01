from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def payment_admin_kb(payment_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm_{payment_id}"),
         InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{payment_id}")]
    ])

def admin_panel_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
        [InlineKeyboardButton(text="💳 Платежи", callback_data="payments")],
        [InlineKeyboardButton(text="📤 Выводы", callback_data="withdraws")]
    ])
