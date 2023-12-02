from django.http import HttpResponse


class AuthenticateUser:
    def __init__(self):
        self.__user = None

    def get_user(self, user):
        if self.__user:
            return user
        else:
            return HttpResponse("<h1>Sem contexto (204)</h1>")

