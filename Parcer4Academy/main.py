import asyncio, os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
import pandas as pd
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

download_dir = "files"
os.makedirs(download_dir, exist_ok=True)



@dp.message(Command("start"))
async def start(message: Message):
    await bot.send_message(message.chat.id, "Скиньте")

async def menu(message: Message):
    text = """<b>📗Парсер Excel таблиц📗</b> \nВыберите действие: """
    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗓️Отчет по выставленному расписанию🗓️", callback_data="schedule")],
        [InlineKeyboardButton(text="💡Отчет по темам занятия💡", callback_data="lesson_theme")],
        [InlineKeyboardButton(text="👥Отчет по студентам👥", callback_data="students")],
        [InlineKeyboardButton(text="🚶🏻‍➡️Отчет по посещаемости студентов🚶🏻‍➡️", callback_data="attendance")],
        [InlineKeyboardButton(text="✅Отчет по проверенным домашним заданиям✅", callback_data="test_homework")],
        [InlineKeyboardButton(text="⏳Отчет по сданным домашним заданиям⏳", callback_data="succeed_homework")],
        [InlineKeyboardButton(text="🔙Назад🔙", callback_data="back")]
    ])
    photo = FSInputFile('img/academy_logo.jpg')
    await message.answer_photo(photo, caption=text, parse_mode="HTML", reply_markup=markup_menu)


@dp.message(F.document)
async def get_excel(message: Message):
    document = message.document

    if not document.file_name.endswith(".xlsx"):
        await message.answer("Неверный формат файла!", show_alert=True)
        return

    file_path = os.path.join(download_dir, document.file_name)

    file = await bot.get_file(document.file_id)
    await bot.download_file(file.file_path, file_path)

    try:
        df = pd.read_excel(file_path)

        if df.empty:
            await message.answer("Файл пустой", show_alert=True)
            return

        text = "📄 Содержимое файла:\n\n"

        for index, row in df.iterrows():
            row_text = " | ".join(str(cell) for cell in row.values)
            text += f"{index + 1}. {row_text}\n"

            if len(text) > 3500:
                text += "\n⚠️ Данные обрезаны"
                break
        await message.answer(text)

    except Exception as e:
        await message.answer(f"Ошибка при чтении файла:\n{e}")

    finally:
        os.remove(file_path)

@dp.callback_query(F.data.startswith("schedule"))
async def f_schedule(call: CallbackQuery):
    pass



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

