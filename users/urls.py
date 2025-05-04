from django.urls import path, reverse_lazy
from .views import login, profile, logout, UserRegistrationView, EmailVerificationView, MyPasswordResetView,MyPasswordResetForm, MyPasswordResetConfirmView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'users'  # Эта строка нужна для работы namespace!

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path(
        'password-reset/',
        MyPasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html',
            success_url=reverse_lazy('users:password_reset_done')
        ),
        name="password_reset"
    ),
    path(
        'password-reset/done/',
        PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name="password_reset_done"
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        MyPasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')
        ),
        name="password_reset_confirm"
    ),
    path(
        'password-reset/complete/',
        PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name="password_reset_complete"
    ),
    path(
        'verify/<str:email>/<uuid:code>/',
        EmailVerificationView.as_view(),
        name='email_verifications'
    ),
]
