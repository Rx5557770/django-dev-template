from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=150, min_length=4)
    password = forms.CharField(widget=forms.PasswordInput, label="密码", min_length=6)
    remember = forms.BooleanField(required=False, label="记住我")


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=150, min_length=4)
    password = forms.CharField(widget=forms.PasswordInput, label="密码", min_length=6)
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="确认密码", min_length=6
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("两次密码不一致")
        return cleaned_data
