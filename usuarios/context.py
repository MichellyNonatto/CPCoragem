from django.http import HttpResponse
# Estou modificando ainda

class AuthenticateUser:
    def __init__(self):
        self.__user = None

    def get_user(self, user):
        if self.__user:
            return user
        else:
            return HttpResponse("'error/error_204.html'")

