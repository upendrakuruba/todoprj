from django.urls import path
from .views import *
urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", Login_user, name="login"),
    path("logout/", Logout_user, name="logout"),
    path("forgotpassword/", forgotpassword, name="forgotpassword"),
    path("resetpassword_validate/<uidb64>/<token>/", resetpassword_validate, name="resetpassword_validate"),
    path("resetpassword/", resetpassword, name="resetpassword"),


]
