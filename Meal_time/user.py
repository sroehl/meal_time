import werkzeug.security


class User():

    def __init__(self, username):
        self.username = username
        self.email = None


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_annoymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return werkzeug.security.check_password_hash(password_hash, password)
