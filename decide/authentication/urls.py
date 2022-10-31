from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from authentication import views

from .views import GetUserView, LogoutView, RegisterView, SignInView


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('signin/', SignInView.sing_in, name='signin'),
    path('hello/', SignInView.hello, name='hello'),
    #path('signout/', SignInView.sign_out, name='signout'),
]
