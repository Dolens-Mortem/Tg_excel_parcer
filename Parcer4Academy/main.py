import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import pandas as pd
from config import BOT_TOKEN, PASSWORD
from users import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class AuthState(StatesGroup):
    waiting_for_password = State()
    waiting_for_limit = State()


async def create_profile(message: Message):
    lang = get_lang(message.from_user.id)
    await bot.send_message(message.chat.id, lang.welcome_text, parse_mode="HTML")


@dp.message(Command("start"))
async def start(message, state: FSMContext):
    await user_init(message.from_user.id)
    defender = get_entering(message.from_user.id)
    if defender.antispam:
        return

    defender.set_antispam(True)

    if not defender.security:
        lang = get_lang(message.from_user.id)
        await bot.send_message(message.chat.id, lang.enter_password)
        await state.set_state(AuthState.waiting_for_password)
        await state.update_data()
    else:
        defender.set_antispam(False)
        await create_profile(message)


@dp.message(AuthState.waiting_for_password)
async def set_password(message, state: FSMContext):
    defender = get_entering(message.from_user.id)
    await state.clear()
    if defender.password_check(PASSWORD, message.text):
        await create_profile(message)
    else:
        lang = get_lang(message.from_user.id)
        await message.answer(lang.wpass_text) #"Неверный пароль! Введите еще раз: "
        await state.set_state(AuthState.waiting_for_password)
        await state.update_data()
        return


@dp.message(F.document)
async def get_excel(message: Message):
    defender = get_entering(message.from_user.id)
    excel_parcer = get_excel_parcer(message.from_user.id)
    print(excel_parcer)
    print(defender)
    file_path = excel_parcer.path

    if not defender.security:
        return
    document = message.document
    if not document.file_name.endswith((".xls", ".xlsx")):
        lang = get_lang(message.from_user.id)
        await message.answer(lang.wformat_text, show_alert=True) #"Неверный формат файла!"
        return

    file = await bot.get_file(document.file_id)
    await bot.download_file(file.file_path, file_path)
    print('Файл получен')

    await menu(message)

    #os.remove(file_path)


async def menu(message: Message):
    lang = get_lang(message.chat.id)
    print("menu : ", lang.language, " chatid : ", message.chat.id)
    text = lang.menu_text
    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=lang.loaded_file, callback_data="_"),
            InlineKeyboardButton(text=lang.loaded_file, callback_data="_"),
        ],
        [InlineKeyboardButton(text=lang.menu_btn1_text, callback_data="schedule")],
        [InlineKeyboardButton(text=lang.menu_btn2_text, callback_data="lesson_theme")],
        [InlineKeyboardButton(text=lang.menu_btn3_text, callback_data="students")],
        [InlineKeyboardButton(text=lang.menu_btn4_text, callback_data="attendance")],
        [InlineKeyboardButton(text=lang.menu_btn5_text, callback_data="test_homework")],
        [InlineKeyboardButton(text=lang.menu_btn6_text, callback_data="succeed_homework")],
        [InlineKeyboardButton(text=lang.selected_language, callback_data="lang")],
        [InlineKeyboardButton(text=lang.menu_back_text, callback_data="back")]
    ])
    photo = FSInputFile('img/academy_logo.jpg')
    await message.answer_photo(photo=photo, caption=text, parse_mode="HTML", reply_markup=markup_menu)


@dp.callback_query(F.data.startswith("schedule"))
async def f_schedule(call: CallbackQuery):
    excel_parcer = get_excel_parcer(call.from_user.id)
    try:
        report = excel_parcer.schedule_count()
        await call.message.answer(report, parse_mode="HTML")
    except Exception as e:
        print(e)

@dp.callback_query(F.data.startswith("lesson_theme"))
async def f_lesson_theme(call: CallbackQuery, state: FSMContext):
    lang = get_lang(call.from_user.id)
    await bot.send_message(call.message.chat.id, lang.enter_limits)
    await state.set_state(AuthState.waiting_for_limit)
    await state.update_data()

@dp.message(AuthState.waiting_for_limit)
async def set_limit(message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    excel_parcer = get_excel_parcer(message.from_user.id)
    await state.clear()
    limit = int(message.text)
    if limit > 4000 or limit <= 0:
        await message.answer(lang.wformat_limit_text)
        await state.set_state(AuthState.waiting_for_limit)
        await state.update_data()
        return
    else:
        report = excel_parcer.check_themes(limit=limit)
        if not report:
            await message.answer(lang.g_lesson_theme_text)
        else:
            text = lang.lesson_theme_report
            text += "\n".join(report)
            chunks = []
            current = ""
            for line in text.split("\n"):
                if len(current) + len(line) + 1 > 4000:
                    chunks.append(current)
                    current = ""
                current += line + "\n"
            if current:
                chunks.append(current)
            for chunk in chunks:
                await message.answer(chunk, parse_mode="HTML")


@dp.callback_query(F.data.startswith("students"))
async def f_students(call: CallbackQuery):
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)
    report = excel_parcer.lower_student_check()
    if not report:
        await call.message.answer(lang.g_students_text)
    else:
        text = lang.students_report
        text += "\n".join(report)
        await call.message.answer(text, parse_mode="HTML")

@dp.callback_query(F.data.startswith("attendance"))
async def f_attendance(call: CallbackQuery):
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)
    report = excel_parcer.lower_teacher_check()
    if not report:
        await call.message.answer(lang.g_attendance_text)
    else:
        text = lang.attendance_report
        text += "\n".join(report)
        await call.message.answer(text, parse_mode="HTML")


@dp.callback_query(F.data.startswith("lang"))
async def f_lang(call: CallbackQuery):
    lang = get_lang(call.from_user.id)
    if lang.language == "ru":
        lang.set_language("en")
    else:
        lang.set_language("ru")
    await call.message.delete()
    await menu(call.message)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

