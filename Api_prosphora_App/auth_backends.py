from django.contrib.auth.backends import ModelBackend
from .models import User

class NumPhoneBackend(ModelBackend):
    def authenticate(self, request, num_phone=None, password=None, **kwargs):
        if num_phone is None or password is None:
            return None
        try:
            user = User.objects.get(num_phone=num_phone)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password) and user.is_active:
            return user
        return None
