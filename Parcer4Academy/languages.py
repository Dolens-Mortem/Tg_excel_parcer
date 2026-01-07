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
            "wformat_text": "Неверный формат файла!",
            "wpass_text": "Неверный пароль! Введите еще раз: ",
            "selected_language" : "🌐Язык (🇷🇺Русский)"
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
            "wformat_text": "Invalid file format!",
            "wpass_text": "Wrong password! Please, try again: ",
            "selected_language": "🌐Language (🇬🇧English)"
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


