from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import *
from config import TOKEN, ADMIN_ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# -----------------------------
# /start
# -----------------------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer("¡Bienvenido! Usa /menu para ver los productos.")


# -----------------------------
# /menu
# -----------------------------
@dp.message_handler(commands=["menu"])
async def menu(message: types.Message):
    productos = get_products()

    if not productos:
        await message.answer("No hay productos disponibles aún.")
        return

    kb = InlineKeyboardMarkup()

    for p in productos:
        kb.add(InlineKeyboardButton(p[1], callback_data=f"prod_{p[0]}"))

    await message.answer("Selecciona un producto:", reply_markup=kb)


# -----------------------------
# Opciones del producto
# -----------------------------
@dp.callback_query_handler(lambda c: c.data.startswith("prod_"))
async def product_options(callback: types.CallbackQuery):
    product_id = callback.data.split("_")[1]
    opciones = get_product_options(product_id)

    if not opciones:
        await callback.message.answer("Este producto no tiene opciones aún.")
        return

    kb = InlineKeyboardMarkup()

    for op in opciones:
        name = op[2]
        price = op[3]
        stock = op[4]
        kb.add(InlineKeyboardButton(f"{name} - ${price} (Stock: {stock})", callback_data=f"opt_{op[0]}"))

    await callback.message.answer("Opciones disponibles:", reply_markup=kb)


# -----------------------------
# Panel admin
# -----------------------------
@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("No tienes permisos.")

    await message.answer("Panel administrador (por completar).")


# -----------------------------
# INICIO DEL BOT (Render)
# -----------------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
