class Language:
    welcome_text: str
    enter_password: str
    menu_text: str
    menu_btn1_text: str
    menu_btn2_text: str
    menu_btn3_text: str
    menu_btn4_text: str
    menu_btn5_text: str
    menu_btn6_text: str
    menu_back_text: str
    wformat_text: str
    wpass_text: str
    selected_language: str
    enter_limits : str
    wformat_limit_text : str
    g_lesson_theme_text : str
    lesson_theme_report : str
    g_students_text : str
    students_report : str
    g_attendance_text : str
    attendance_report : str
    loaded_file : str
    unloaded_file : str
    delete_file_text : str
    first_menu1 : str
    first_menu2 : str
    settings_text1 : str
    settings_text2 : str
    text_for_testing : str
    week_text : str
    month_text : str

    TRANSLATIONS = {
        "ru": {
            "welcome_text": "<b>Добро пожаловать</b> \nПришлите excel файл (с форматом .xlsx)",
            "enter_password": "Для входа введите пароль: ",
            "menu_text": "<b>📗Парсер Excel таблиц📗</b> \nВыберите действие: ",
            "menu_btn1_text": "🗓️Отчет по выставленному расписанию🗓️",
            "menu_btn2_text": "💡Отчет по темам занятия💡",
            "menu_btn3_text": "👥Отчет по студентам👥",
            "menu_btn4_text": "🚶🏻‍➡️Отчет по посещаемости студентов🚶🏻‍➡️",
            "menu_btn5_text": "✅Отчет по проверенным домашним заданиям✅",
            "menu_btn6_text": "⏳Отчет по сданным домашним заданиям⏳",
            "menu_back_text": "🔙Назад🔙",
            "wformat_text": "Неверный формат файла! Отправьте файл ещё раз: ",
            "wpass_text": "Неверный пароль! Введите еще раз: ",
            "selected_language" : "🌐Язык (🇷🇺Русский)",
            "enter_limits" : "Введите кол-во выводимых студентов (не более 3500 человек): ",
            "wformat_limit_text" : "Неверный формат, введите ещё раз: ",
            "g_lesson_theme_text" : "Все темы соответствуют формату",
            "lesson_theme_report" : "Темы с неверным форматом:\n\n",
            "g_students_text": "У студентов хорошие оценки!",
            "students_report": "Студенты с низкими оценками:\n\n",
            "g_attendance_text": "У преподавателей хорошая посещаемость!",
            "attendance_report": "Преподаватели с низкой посещаемостью:\n\n",
            "loaded_file": "Файл загружен!✅",
            "unloaded_file": "Загрузите файл!❔",
            "delete_file_text": "🗑️Удалить файл",
            "first_menu1": "▶️Запустить парсер▶️",
            "first_menu2": "⚙️Настройки⚙️",
            "settings_text1": "Выгрузка: 📄 Файлом .txt 📄",
            "settings_text2": "Выгрузка: 💬 Сообщением 💬",
            "text_for_testing": "Статистику за какое время вы хотите проверить?",
            "week_text": "За неделю",
            "month_text": "За месяц"
        },

        "en": {
            "welcome_text": "<b>Welcome</b>\nPlease send an excel file (.xlsx)",
            "enter_password": "Enter password:",
            "menu_text": "<b>📗Excel Parcer📗</b> \nChoose an action: ",
            "menu_btn1_text": "🗓️Schedule report🗓️",
            "menu_btn2_text": "💡Lesson topic schedule💡",
            "menu_btn3_text": "👥Student report👥",
            "menu_btn4_text": "🚶🏻‍➡️Student attendance report🚶🏻‍➡️",
            "menu_btn5_text": "✅Checked homework report✅",
            "menu_btn6_text": "⏳Submitted homework report⏳",
            "menu_back_text": "🔙Return🔙",
            "wformat_text": "Invalid file format! Please, try again: ",
            "wpass_text": "Wrong password! Please, try again: ",
            "selected_language": "🌐Language (🇬🇧English)",
            "enter_limits": "Enter the number of students to be displayed (no more than 3500): ",
            "wformat_limit_text": "Invalid format! Please, try again: ",
            "g_lesson_theme_text": "All topics correspond to the format",
            "lesson_theme_report": "Topics with the wrong format:\n\n",
            "g_students_text": "The students have good grades!",
            "students_report": "Students with low grades:\n\n",
            "g_attendance_text": "The teachers have good attendance!",
            "attendance_report": "Teachers with low attendance:\n\n",
            "loaded_file": "File is loaded!✅",
            "unloaded_file": "Upload the file!❔",
            "delete_file_text": "🗑️Delete the file",
            "first_menu1": "▶️Execute parcer▶️",
            "first_menu2": "⚙️Settings⚙️",
            "settings_text1": "Uploading: 📄 With .txt file 📄",
            "settings_text2": "Uploading: 💬 With Telegram message 💬",
            "text_for_testing": "What time period do you want to check?",
            "week_text": "Per week",
            "month_text": "Per month"
        }
    }

    def __init__(self, language: str = "ru"):
        self.language = language
        self.set_language(language)

    def set_language(self, language: str):
        self.language = language
        self.apply()

    def apply(self):
        texts = self.TRANSLATIONS[self.language]
        for key, value in texts.items():
            setattr(self, key, value)


