from aiogram import Router, types, F
from aiogram.filters import Command
from config import ADMIN_ID, TARIFFS, VPN_LINK
from database import (
    get_pending_payments, get_payment_by_id,
    confirm_payment, reject_payment, activate_vpn, add_balance, get_user_referrer
)
from keyboards.admin_kb import admin_panel_kb, payment_admin_kb

router = Router()

def is_admin(user_id):
    return user_id == ADMIN_ID

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет доступа.")
        return
    await message.answer("👨‍💼 <b>Панель администратора</b>\n\nВыберите раздел:",
        parse_mode="HTML", reply_markup=admin_panel_kb())

@router.callback_query(F.data == "stats")
async def show_stats(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    import aiosqlite
    async with aiosqlite.connect("vpn.db") as db:
        total_users = (await (await db.execute("SELECT COUNT(*) FROM users")).fetchone())[0]
        paid_users = (await (await db.execute("SELECT COUNT(*) FROM users WHERE paid=1")).fetchone())[0]
        pending = (await (await db.execute("SELECT COUNT(*) FROM payments WHERE status='pending'")).fetchone())[0]
        confirmed = (await (await db.execute("SELECT COUNT(*) FROM payments WHERE status='confirmed'")).fetchone())[0]
        total_income = (await (await db.execute("SELECT SUM(amount) FROM payments WHERE status='confirmed'")).fetchone())[0] or 0
    await callback.message.edit_text(
        f"📊 <b>Статистика</b>\n\n"
        f"👤 Всего пользователей: <b>{total_users}</b>\n"
        f"✅ С активной подпиской: <b>{paid_users}</b>\n\n"
        f"⏳ Ожидают подтверждения: <b>{pending}</b>\n"
        f"✅ Подтверждённых платежей: <b>{confirmed}</b>\n"
        f"💰 Общий доход: <b>{total_income} ₽</b>",
        parse_mode="HTML", reply_markup=admin_panel_kb()
    )
    await callback.answer()

@router.callback_query(F.data == "payments")
async def show_payments(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    payments = await get_pending_payments()
    if not payments:
        await callback.message.edit_text("💳 Ожидающих платежей нет.", reply_markup=admin_panel_kb())
    else:
        await callback.message.edit_text(
            f"💳 <b>Ожидающих платежей: {len(payments)}</b>\n\nЧеки отправлены отдельными сообщениями.",
            parse_mode="HTML", reply_markup=admin_panel_kb()
        )
    await callback.answer()

@router.callback_query(F.data == "withdraws")
async def show_withdraws(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    import aiosqlite
    async with aiosqlite.connect("vpn.db") as db:
        cursor = await db.execute("SELECT * FROM withdraws WHERE status='pending'")
        withdraws = await cursor.fetchall()
    if not withdraws:
        await callback.message.edit_text("📤 Заявок на вывод нет.", reply_markup=admin_panel_kb())
    else:
        text = f"📤 <b>Заявки на вывод: {len(withdraws)}</b>\n\n"
        for w in withdraws:
            text += f"🆔 #{w[0]} | 👤 ID: {w[1]} | 💰 {w[2]} ₽ | 💳 <code>{w[3]}</code>\n"
        await callback.message.edit_text(text, parse_mode="HTML", reply_markup=admin_panel_kb())
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_"))
async def confirm_payment_handler(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    payment_id = int(callback.data.split("_")[1])
    payment = await get_payment_by_id(payment_id)
    if not payment:
        await callback.answer("Платёж не найден", show_alert=True)
        return
    user_id = payment[1]
    tariff = TARIFFS.get(payment[2], {})
