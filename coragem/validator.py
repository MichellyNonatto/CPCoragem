from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from usuarios.models import Funcionario


class LoginForm(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = Funcionario
        print(email)
        try:
            user = UserModel.objects.get(email_empresarial=email)
        except UserModel.DoesNotExist:
            print("1")
            return None

        if user.check_password(password):
            print('2')
            return user
        print('3')
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
