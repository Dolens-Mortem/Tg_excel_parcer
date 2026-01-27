import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from config import BOT_TOKEN, PASSWORD, FAKE_PASSWORD
from users import *

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class AuthState(StatesGroup):
    waiting_for_password = State()
    waiting_for_limit = State()
    waiting_for_excel = State()

async def f_send_message(text, message: Message):
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


async def create_profile(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    if get_file_loaded(message.chat.id):
        await menu(message)
    else:
        await bot.send_message(message.chat.id, lang.welcome_text, parse_mode="HTML")
        await state.set_state(AuthState.waiting_for_excel)
        await state.update_data()


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
        await create_profile(message, state)


@dp.message(AuthState.waiting_for_password)
async def set_password(message, state: FSMContext):
    defender = get_entering(message.from_user.id)
    await state.clear()
    if defender.password_check(FAKE_PASSWORD, message.text):
        await create_profile(message, state)
    else:
        lang = get_lang(message.from_user.id)
        await message.answer(lang.wpass_text) #"Неверный пароль! Введите еще раз: "
        await state.set_state(AuthState.waiting_for_password)
        await state.update_data()
        return


@dp.message(AuthState.waiting_for_excel)
async def get_excel(message: Message, state: FSMContext):
    defender = get_entering(message.from_user.id)
    excel_parcer = get_excel_parcer(message.from_user.id)
    await state.clear()
    file_path = f"{excel_parcer.path}/excel-file"
    if not defender.security:
        return
    document = message.document
    if not document.file_name.endswith((".xls", ".xlsx")):
        lang = get_lang(message.from_user.id)
        await state.set_state(AuthState.waiting_for_excel)
        await state.update_data()
        await message.answer(lang.wformat_text, show_alert=True) #"Неверный формат файла!"
        return

    file = await bot.get_file(document.file_id)
    await bot.download_file(file.file_path, file_path)
    set_file_loaded(message.from_user.id, True)
    print('Файл получен')

    await menu(message)

    #os.remove(file_path)


async def menu(message: Message):
    lang = get_lang(message.chat.id)

    text_loaded = lang.unloaded_file
    if get_file_loaded(message.chat.id):
        text_loaded = lang.loaded_file

    text = lang.menu_text
    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_loaded, callback_data="load"),
            InlineKeyboardButton(text=lang.delete_file_text, callback_data="delete"),
        ],
        [InlineKeyboardButton(text=lang.menu_btn1_text, callback_data="schedule")],
        [InlineKeyboardButton(text=lang.menu_btn2_text, callback_data="lesson_theme")],
        [InlineKeyboardButton(text=lang.menu_btn3_text, callback_data="students")],
        [InlineKeyboardButton(text=lang.menu_btn4_text, callback_data="attendance")],
        [InlineKeyboardButton(text=lang.menu_btn5_text, callback_data="test_homework")],
        [InlineKeyboardButton(text=lang.menu_btn6_text, callback_data="succeed_homework")],
        [InlineKeyboardButton(text=lang.menu_back_text, callback_data="back")]
    ])
    photo = FSInputFile('img/academy_logo.jpg')
    await message.answer_photo(photo=photo, caption=text, parse_mode="HTML", reply_markup=markup_menu)


@dp.callback_query(F.data.startswith("delete"))
async def f_delete(call: CallbackQuery):
    if not get_file_loaded(call.from_user.id):
        await call.answer("Файл не загружен!", show_alert=True)
        return
    delete_excel_file(call.from_user.id)
    await call.message.delete()
    await menu(call.message)


@dp.callback_query(F.data.startswith("load"))
async def f_load(call: CallbackQuery, state: FSMContext):
    lang = get_lang(call.from_user.id)
    await call.message.answer(lang.welcome_text, parse_mode="HTML")
    await state.set_state(AuthState.waiting_for_excel)
    await state.update_data()


@dp.callback_query(F.data.startswith("schedule"))
async def f_schedule(call: CallbackQuery):
    if not get_file_loaded(call.from_user.id):
        await call.answer("Файл не загружен!", show_alert=True)
        return
    excel_parcer = get_excel_parcer(call.from_user.id)
    try:
        report = excel_parcer.schedule_count()
        if excel_parcer.is_txt_file:
            with open(f"{excel_parcer.path}/report.txt", "a", encoding="utf-8") as f:
                f.write(text)
            await call.message.answer_document(FSInputFile(f"{excel_parcer.path}/report.txt"), caption="<b>Отсчет</b>", parse_mode="HTML")
            f.close()
            os.remove(f"{excel_parcer.path}/report.txt")

        else:
            await call.message.answer(report, parse_mode="HTML")
    except Exception as e:
        print(e)


@dp.callback_query(F.data.startswith("lesson_theme"))
async def f_lesson_theme(call: CallbackQuery, state: FSMContext):
    if not get_file_loaded(call.from_user.id):
        await call.answer("Файл не загружен!", show_alert=True)
        return
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
            if excel_parcer.is_txt_file:
                with open(f"{excel_parcer.path}/report.txt", "a", encoding="utf-8") as f:
                    f.write(text)
                await message.answer_document(FSInputFile(f"{excel_parcer.path}/report.txt"), caption="<b>Отсчет</b>", parse_mode="HTML")
                f.close()

                os.remove(f"{excel_parcer.path}/report.txt")
            else:
                await f_send_message(text, message=message)


@dp.callback_query(F.data.startswith("students"))
async def f_students(call: CallbackQuery):
    if not get_file_loaded(call.from_user.id):
        await call.answer("Файл не загружен!", show_alert=True)
        return
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)
    report = excel_parcer.lower_student_check()
    if not report:
        await call.message.answer(lang.g_students_text)
    else:
        text = lang.students_report
        text += "\n".join(report)
        if excel_parcer.is_txt_file:
            with open(f"{excel_parcer.path}/report.txt", "a", encoding="utf-8") as f:
                f.write(text)
            await call.message.answer_document(FSInputFile(f"{excel_parcer.path}/report.txt"), caption="<b>Отсчет</b>", parse_mode="HTML")
            f.close()

            os.remove(f"{excel_parcer.path}/report.txt")
        else:
            await f_send_message(text, message=call.message)


@dp.callback_query(F.data.startswith("attendance"))
async def f_attendance(call: CallbackQuery):
    if not get_file_loaded(call.from_user.id):
        await call.answer("Файл не загружен!", show_alert=True)
        return
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)
    report = excel_parcer.lower_teacher_check()
    if not report:
        await call.message.answer(lang.g_attendance_text)
    else:
        text = lang.attendance_report
        text += "\n".join(report)
        if excel_parcer.is_txt_file:
            with open(f"{excel_parcer.path}/report.txt", "a", encoding="utf-8") as f:
                f.write(text)
            await call.message.answer_document(FSInputFile(f"{excel_parcer.path}/report.txt"), caption="<b>Отсчет</b>", parse_mode="HTML")
            f.close()
            os.remove(f"{excel_parcer.path}/report.txt")
        else:
            await f_send_message(text, message=call.message)


@dp.callback_query(F.data.startswith("test_homework"))
async def f_test_homework(call: CallbackQuery):
    lang = get_lang(call.from_user.id)
    text = lang.text_for_testing
    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=lang.month_text, callback_data="month"),
            InlineKeyboardButton(text=lang.week_text, callback_data="week"),
        ]
    ])
    await call.message.edit_caption(caption=text, reply_markup=markup_menu, parse_mode="HTML")


@dp.callback_query(F.data.startswith("month"))
async def f_month(call: CallbackQuery):
    await call.message.delete()
    await menu(call.message)
    await f_testing_homework(call=call, period="month")


@dp.callback_query(F.data.startswith("week"))
async def f_week(call: CallbackQuery):
    await call.message.delete()
    await menu(call.message)
    await f_testing_homework(call=call, period="week")


async def f_testing_homework(call: CallbackQuery, period):
    if not get_file_loaded(call.from_user.id):
        await call.answer("Файл не загружен!", show_alert=True)
        return
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)
    report = excel_parcer.testing_homework(period=period)
    if not report:
        await call.message.answer(lang.g_attendance_text)
    else:
        text = ""
        text += "\n".join(report)
        if excel_parcer.is_txt_file:
            with open(f"{excel_parcer.path}/report.txt", "a", encoding="utf-8") as f:
                f.write(text)
            await call.message.answer_document(FSInputFile(f"{excel_parcer.path}/report.txt"), caption="<b>Отсчет</b>", parse_mode="HTML")
            f.close()
            os.remove(f"{excel_parcer.path}/report.txt")
        else:
            await f_send_message(text, message=call.message)



@dp.callback_query(F.data.startswith("succeed_homework"))
async def f_succeed_homework(call: CallbackQuery):
    if not get_file_loaded(call.from_user.id):
        await call.answer("Файл не загружен!", show_alert=True)
        return
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)
    report = excel_parcer.lower_homework()
    if not report:
        await call.message.answer(lang.g_attendance_text)
    else:
        text = ""
        text += "\n".join(report)
        if excel_parcer.is_txt_file:
            with open(f"{excel_parcer.path}/report.txt", "a", encoding="utf-8") as f:
                f.write(text)
            await call.message.answer_document(FSInputFile(f"{excel_parcer.path}/report.txt"), caption="<b>Отсчет</b>", parse_mode="HTML")
            f.close()
            os.remove(f"{excel_parcer.path}/report.txt")
        else:
            await f_send_message(text, message=call.message)



@dp.callback_query(F.data.startswith("lang"))
async def f_lang(call: CallbackQuery):
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)
    if lang.language == "ru":
        lang.set_language("en")
    else:
        lang.set_language("ru")

    lang = get_lang(call.from_user.id)
    text_loaded = lang.settings_text1
    if not excel_parcer.is_txt_file:
        text_loaded = lang.settings_text2

    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang.selected_language, callback_data="lang")],
        [InlineKeyboardButton(text=text_loaded, callback_data="uploading")],
        [InlineKeyboardButton(text=lang.menu_back_text, callback_data="back")]
    ])
    await call.message.edit_caption(caption=lang.menu_text, reply_markup=markup_menu, parse_mode="HTML")


@dp.callback_query(F.data.startswith("back"))
async def f_back(call: CallbackQuery):
    lang = get_lang(call.from_user.id)
    text_loaded = lang.unloaded_file
    if get_file_loaded(call.message.chat.id):
        text_loaded = lang.loaded_file

    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text_loaded, callback_data="load"),
            InlineKeyboardButton(text=lang.delete_file_text, callback_data="delete"),
        ],
        [InlineKeyboardButton(text=lang.first_menu1, callback_data="acting")],
        [InlineKeyboardButton(text=lang.first_menu2, callback_data="settings")]
    ])
    await call.message.edit_caption(caption=lang.menu_text, reply_markup=markup_menu, parse_mode="HTML")


@dp.callback_query(F.data.startswith("acting"))
async def f_acting(call: CallbackQuery):
    await call.message.delete()
    await menu(call.message)


@dp.callback_query(F.data.startswith("settings"))
async def f_settings(call: CallbackQuery):
    lang = get_lang(call.from_user.id)
    excel_parcer = get_excel_parcer(call.from_user.id)

    text_loaded = lang.settings_text1
    if not excel_parcer.is_txt_file:
        text_loaded = lang.settings_text2

    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang.selected_language, callback_data="lang")],
        [InlineKeyboardButton(text=text_loaded, callback_data="uploading")],
        [InlineKeyboardButton(text=lang.menu_back_text, callback_data="back")]
    ])
    await call.message.edit_caption(caption=lang.menu_text, reply_markup=markup_menu, parse_mode="HTML")


@dp.callback_query(F.data.startswith("uploading"))
async def f_uploading(call: CallbackQuery):
    excel_parcer = get_excel_parcer(call.from_user.id)

    if excel_parcer.is_txt_file:
        excel_parcer.is_txt_file = False
    else:
        excel_parcer.is_txt_file = True

    lang = get_lang(call.from_user.id)

    text_loaded = lang.settings_text1
    if not excel_parcer.is_txt_file:
        text_loaded = lang.settings_text2

    markup_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lang.selected_language, callback_data="lang")],
        [InlineKeyboardButton(text=text_loaded, callback_data="uploading")],
        [InlineKeyboardButton(text=lang.menu_back_text, callback_data="back")]
    ])
    await call.message.edit_caption(caption=lang.menu_text, reply_markup=markup_menu, parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

