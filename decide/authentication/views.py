from authentication.form import NewUserForm
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED,
        HTTP_400_BAD_REQUEST,
        HTTP_401_UNAUTHORIZED
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import  login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .serializers import UserSerializer

from django.conf import settings

class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)

class SignUpView(APIView):
    def register(request):
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                #messages.success(request, "Registration successful." )
                return redirect("signup")
            else:

                errors = []
                if request.POST['password1'] != request.POST['password2']:
                    differents_passwords = "Passwords don't match"
                    errors.append(differents_passwords)
                if len(request.POST['password1']) < 8:
                    short_password = "Password must be at least 8 characters"
                    errors.append(short_password)
                if request.POST['password1'].isdigit():
                    only_numbers = "Password must contain at least one letter"
                    errors.append(only_numbers)
                if request.POST['password1'].isalpha():
                    only_letters = "Password must contain at least one number"
                    errors.append(only_letters)
                if request.POST['first_name'] == "":
                    no_name = "You must enter a name"
                    errors.append(no_name)
                if request.POST['last_name'] == "":
                    no_surname = "You must enter a surname"
                    errors.append(no_surname)
                if request.POST['email'] == "":
                    no_email = "You must enter an email"
                    errors.append(no_email)
                if request.POST['username'] == "":
                    no_username = "You must enter a username"
                    errors.append(no_username)
                if request.POST['first_name'][0].isupper() == False:
                    name_not_capitalized = "Name must be capitalized"
                    errors.append(name_not_capitalized)
                if request.POST['last_name'][0].isupper() == False:
                    surname_not_capitalized = "Surname must be capitalized"
                    errors.append(surname_not_capitalized)

                are_errors = False
                if len(errors) > 0:
                    are_errors = True
                form = NewUserForm()
                
                return render(request, 'signup.html', {
                        'register_form':form ,
                        'errors': errors,
                        'are_errors': are_errors
                        })
        form = NewUserForm()
        return render (request, "signup.html", {
            "register_form":form})

class SignInView(APIView):
            
    def sing_in(request):

        if request.method == 'GET':
            
            return render(request, 'signin.html', {
                'form' : AuthenticationForm
            })
        else:
            print(request.POST)
            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])
            if user is None:

                return render(request, 'signin.html', {
                    'form' : AuthenticationForm,
                    'error': 'Username or password is incorrect'
                })
            else:
                login(request, user)
                return redirect('hello')

    


    def hello(request):

        return render(request, 'hello.html', {
                'username' : request.user
            })

    def sign_out(request):
       logout(request)
       return redirect('signin')
