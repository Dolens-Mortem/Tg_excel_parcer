import os
from defender import Defender
from languages import Language
from parcer import ExcelParcer

user_account = {}

async def user_init(user_id):
    if user_id not in user_account:
        download_dir = f"files/{user_id}"
        os.makedirs(download_dir, exist_ok=True)
        user_account[user_id] = {
            "language" : Language("ru"),
            "isEnter" : Defender(),
            "excelParcer" : ExcelParcer(download_dir),
            "isFileLoaded" : False
        }
    print(user_account)

def get_lang(user_id):
    return user_account[user_id]["language"]

def get_entering(user_id):
    return user_account[user_id]["isEnter"]

def get_excel_parcer(user_id):
    return user_account[user_id]["excelParcer"]

def get_file_loaded(user_id):
    return user_account[user_id]["isFileLoaded"]

def set_file_loaded(user_id, condition: bool):
    user_account[user_id]["isFileLoaded"] = condition

def delete_excel_file(user_id):
    download_dir = f"files/{user_id}"
    os.remove(f"{download_dir}/excel-file")
    user_account[user_id]["isFileLoaded"] = False

