import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm, PasswordResetForm, SetPasswordForm)
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Enter your user name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": 'Enter your password'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control py-4"


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter a name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter last name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Enter your user name"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': "Enter your e-mail address"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Enter your password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Confirm password"}))

    class Meta:
        model = User
        fields = ("first_name", 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=48)
        recored = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        recored.send_verification_email()
        return user

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control py-4"


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', "first_name", 'last_name', 'image')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control py-4"
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Enter your e-mail address'
    }))

class MyPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'placeholder': "Enter your password", 'class': 'form-control py-4'})
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'placeholder': "Confirm password", 'class': 'form-control py-4'})
    )