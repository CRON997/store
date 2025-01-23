from django.urls import path

from users.views import (EmailVerificationView, UserRegistrationView, login,
                         logout, profile)

app_name = 'users'
urlpatterns = [
    path('login/',login,name='login'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('profile/',profile,name= 'profile'),
    path('logout/',logout,name= 'logout'),
    path('verify/<str:email>/<uuid:code>/',EmailVerificationView.as_view(),name= 'email_verifications'),
    ]