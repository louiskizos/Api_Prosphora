# Api_prosphora_App/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import App_user

class NumPhoneBackend(BaseBackend):
    def authenticate(self, request, num_phone=None, password=None):
        try:
            user = App_user.objects.get(num_phone=num_phone)
            if user.check_password(password):
                return user
        except App_user.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return App_user.objects.get(pk=user_id)
        except App_user.DoesNotExist:
            return None
