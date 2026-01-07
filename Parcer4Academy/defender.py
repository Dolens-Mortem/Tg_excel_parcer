class Defender:
    def __init__(self):
        self.security = False
        self.antispam = False
    def password_check(self, true_password, user_password):
        if true_password == user_password:
            #Проверка прошла успешно, поэтому защита и антиспам пропускают пользователя
            self.security = True
            self.antispam = False
            return True
        else:
            return False
    def set_antispam(self, antispam: bool):
        self.antispam = antispam