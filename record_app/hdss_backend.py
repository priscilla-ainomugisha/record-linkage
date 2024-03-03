from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

class HdssStaffAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Check if the user exists in the second custom model (Hdss_staff)
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # If the user doesn't exist in the second model, try the first model
            UserModel = get_user_model()  # Using default user model
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                # Redirect to login view with a message to create an account
                messages.warning(request, "Account does not exist. Please create an account.")
                return redirect(reverse('hdss_staff_login'))

        if user.check_password(password) and user.is_active:
            return user
        else:
            return None
