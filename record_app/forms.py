# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from record_app.models import Facility_staff

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Facility_staff
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
