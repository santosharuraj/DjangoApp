from django.urls import path
from api import views

urlpatterns = [
    path('register/',views.UserRegistrationView.as_view() ,name='register'),
    path('login/',views.UserLoginView.as_view() ,name='login'),
    path('profile/',views.UserProfileView.as_view() ,name='profile'),
    path('changepassword/',views.UserChangePasswordView.as_view() ,name='changepassword'),
    path('resetpassword/',views.SendPasswordResetEmailView.as_view() ,name='restpassword'),
    path('resetpassword/<uid>/<token>/',views.UserPasswordResetView.as_view() ,name='restpasswordnow'),

 
]
