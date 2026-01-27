import pandas as pd
import re
from collections import Counter

class ExcelParcer:
    def __init__(self, path):
        self.path = path
        self.is_txt_file = False

    def schedule_count(self):
        df = pd.read_excel(f"{self.path}/excel-file")
        subjects = []
        for col in df.columns:
            for cell in df[col]:
                if isinstance(cell, str) and "Предмет:" in cell:
                    match = re.search(r"Предмет:\s*(.+)", cell)
                    if match:
                        subj = match.group(1).strip()
                        subjects.append(subj)

        counter = Counter(subjects)
        if not counter:
            return "В расписании не найдено ни одной пары"

        text = "<b>Отчёт по расписанию:</b>\n\n"
        for subj, count in counter.items():
            if self.is_txt_file:
                text += f"• {count} пар — {subj} \n"
            else:
                text += f"• <b>{count} пар</b> — {subj} \n"
        return text


    def check_themes(self, limit=3000):
        pattern = re.compile(r"^Урок\s*№\s*\d+\.\s*Тема:\s*.+$")
        df = pd.read_excel(f"{self.path}/excel-file")
        subjects = []
        column_name = df.columns
        for index, row in df.iterrows():
            theme = str(row.iloc[5]).strip()
            if not pattern.match(theme):
                if self.is_txt_file:
                    subjects.append(f"\n• Строка {index + 2}: "
                                    f"\n{column_name[0]}: {row.iloc[0]} "
                                    f"\n{column_name[1]} : {row.iloc[1]} "
                                    f"\n{column_name[2]} : {row.iloc[2]} "
                                    f"\n{column_name[3]} : {row.iloc[3]} "
                                    f"\n{column_name[4]} : {row.iloc[4]} "
                                    f"\n{column_name[5]} : {theme}\n")
                else:
                    subjects.append(f"\n• <u><b>Строка {index+2}:</b></u> "
                                    f"\n{column_name[0]}: {row.iloc[0]} "
                                    f"\n{column_name[1]} : {row.iloc[1]} "
                                    f"\n{column_name[2]} : {row.iloc[2]} "
                                    f"\n{column_name[3]} : {row.iloc[3]} "
                                    f"\n{column_name[4]} : {row.iloc[4]} "
                                    f"\n{column_name[5]} : <b>{theme}</b>\n")
                limit -= 1
            if limit <= 0: break
        return subjects

    def lower_student_check(self):
        df = pd.read_excel(f"{self.path}/excel-file")
        student = []
        column_name = df.columns
        for index, row in df.iterrows():
            try:
                homework_mark = int(row.iloc[15])
                classwork_mark = int(row.iloc[16])
            except Exception as e:
                continue
            if homework_mark <= 1 or classwork_mark < 3:
                if self.is_txt_file:
                    student.append(f"\n• Строка {index + 2}: "
                                   f"\n{column_name[0]}: {row.iloc[0]}"
                                   f"\n{column_name[1]} : {row.iloc[1]}"
                                   f"\n{column_name[2]} : {row.iloc[2]}"
                                   f"\n{column_name[6]} : {row.iloc[6]}"
                                   f"\n{column_name[7]} : {row.iloc[7]}"
                                   f"\n{column_name[8]} : {row.iloc[8]}"
                                   f"\n{column_name[13]} : {row.iloc[13]}"
                                   f"\n{column_name[15]} : {row.iloc[15]}"
                                   f"\n{column_name[16]} : {row.iloc[16]}"
                                   f"\n{column_name[17]} : {row.iloc[17]}\n")
                else:
                    student.append(f"\n• <u><b>Строка {index+2}:</b></u> "
                                    f"\n{column_name[0]}: {row.iloc[0]}"
                                    f"\n{column_name[1]} : {row.iloc[1]}"
                                    f"\n{column_name[2]} : {row.iloc[2]}"
                                    f"\n{column_name[6]} : {row.iloc[6]}"
                                    f"\n{column_name[7]} : {row.iloc[7]}"
                                    f"\n{column_name[8]} : {row.iloc[8]}"
                                    f"\n{column_name[13]} : {row.iloc[13]}"
                                    f"\n{column_name[15]} : {row.iloc[15]}"
                                    f"\n{column_name[16]} : {row.iloc[16]}"
                                    f"\n{column_name[17]} : {row.iloc[17]}\n")
        return student

    def lower_teacher_check(self):
        df = pd.read_excel(f"{self.path}/excel-file")
        teacher = []
        column_name = df.columns
        for index, row in df.iterrows():
            attendance = str(row.iloc[10]).replace("%", "")
            try:
                attendance = int(attendance)
            except Exception as e:
                continue
            if attendance < 40:
                if self.is_txt_file:
                    teacher.append(f"\n• Строка {index + 2}: "
                                   f"\n{column_name[0]}: {row.iloc[0]}"
                                   f"\n{column_name[10]} : {row.iloc[10]}"
                                   f"\n{column_name[11]} : {int(row.iloc[11])}"
                                   f"\n{column_name[12]} : {int(row.iloc[12])}\n")
                else:
                    teacher.append(f"\n• <u><b>Строка {index+2}:</b></u> "
                                    f"\n{column_name[0]}: {row.iloc[0]}"
                                    f"\n{column_name[10]} : {row.iloc[10]}"
                                    f"\n{column_name[11]} : {int(row.iloc[11])}"
                                    f"\n{column_name[12]} : {int(row.iloc[12])}\n")
        return teacher

    def testing_homework(self, period):
        df = pd.read_excel(f"{self.path}/excel-file")
        teacher = []
        column_name = df.columns

        for index, row in df.iterrows():
            if period == "month":
                total = row.iloc[4]
                done = row.iloc[5]
            else:
                total = row.iloc[9]
                done = row.iloc[10]

            try:
                int_total = int(total)
                int_done = int(done)
                percent = (int_done - int_total) / int_total * 100
                percent_diff = 100 + int(percent)
            except Exception as e:
                continue

            if percent_diff < 70:
                if self.is_txt_file:
                    teacher.append(f"\n• Строка {index + 2}: "
                                   f"\n{column_name[1]}: {row.iloc[1]}"
                                   f"\nПолучено : {total}"
                                   f"\nПроверено : {done}"
                                   f"\nПроцент : {percent_diff}\n")
                else:
                    teacher.append(f"\n• <u><b>Строка {index+2}:</b></u> "
                                    f"\n{column_name[1]}: {row.iloc[1]}"
                                    f"\nПолучено : {total}"
                                    f"\nПроверено : {done}"
                                    f"\nПроцент : <b>{percent_diff}</b>\n")
        return teacher

    def lower_homework(self):
        df = pd.read_excel(f"{self.path}/excel-file")
        student = []
        column_name = df.columns
        for index, row in df.iterrows():
            percent = row.iloc[19]
            print(percent)
            try:
                int_percent = int(percent)
            except Exception as e:
                continue
            if int_percent < 70:
                if self.is_txt_file:
                    student.append(f"\n• Строка {index + 2}: "
                                   f"\n{column_name[0]}: {row.iloc[0]}"
                                   f"\n{column_name[1]} : {row.iloc[1]}"
                                   f"\n{column_name[2]} : {row.iloc[2]}"
                                   f"\n{column_name[6]} : {row.iloc[6]}"
                                   f"\n{column_name[7]} : {row.iloc[7]}"
                                   f"\n{column_name[8]} : {row.iloc[8]}"
                                   f"\n{column_name[13]} : {row.iloc[13]}"
                                   f"\n{column_name[15]} : {row.iloc[15]}"
                                   f"\n{column_name[16]} : {row.iloc[16]}"
                                   f"\n{column_name[17]} : {row.iloc[17]}"
                                   f"\n{column_name[19]} : {row.iloc[19]} %\n")
                else:
                    student.append(f"\n• <u><b>Строка {index+2}:</b></u> "
                                    f"\n{column_name[0]}: {row.iloc[0]}"
                                    f"\n{column_name[1]} : {row.iloc[1]}"
                                    f"\n{column_name[2]} : {row.iloc[2]}"
                                    f"\n{column_name[6]} : {row.iloc[6]}"
                                    f"\n{column_name[7]} : {row.iloc[7]}"
                                    f"\n{column_name[8]} : {row.iloc[8]}"
                                    f"\n{column_name[13]} : {row.iloc[13]}"
                                    f"\n{column_name[15]} : {row.iloc[15]}"
                                    f"\n{column_name[16]} : {row.iloc[16]}"
                                    f"\n{column_name[17]} : {row.iloc[17]}"
                                    f"\n{column_name[19]} : <b>{row.iloc[19]} %</b>\n")
        return student
