from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomWidgetMixin:
    def add_custom_widget_attrs(self, field_name, placeholder):
        self.fields[field_name].widget.attrs.update({
            'placeholder': placeholder,
            'class': 'w-full py-4 px-6 rounded-xl'
        })

class LoginForm(AuthenticationForm, CustomWidgetMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_custom_widget_attrs('username', 'Your username')
        self.add_custom_widget_attrs('password', 'Your password')

class SignupForm(UserCreationForm, CustomWidgetMixin):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_custom_widget_attrs('username', 'Your username')
        self.add_custom_widget_attrs('email', 'Your email address')
        self.add_custom_widget_attrs('password1', 'Your password')
        self.add_custom_widget_attrs('password2', 'Repeat password')
