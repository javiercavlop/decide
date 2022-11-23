from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .views import GetUserView, LogoutView, RegisterView, SignUpView, \
    RegisterAPI, SignInView, LoginApi, EditUserView, DeleteUserView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path("signup/", SignUpView.register, name="signup"),
    path('signin/', SignInView.sing_in, name='signin'),
    path('hello/', SignInView.hello, name='hello'),
    path('signout/', SignInView.sign_out, name='signout'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginApi.as_view(), name='login'),
    path('accounts/', include('allauth.urls')),
    path('profile/', EditUserView.edit, name='profile'),
    path('deleteUser/', DeleteUserView.delete, name='deleteUser'),
]
