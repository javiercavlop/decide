from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authtoken.views import ObtainAuthToken
from authentication.form import NewUserForm, UserEditForm
import re
from allauth.socialaccount.models import SocialAccount
from rest_framework import generics, status
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

from .serializers import UserSerializer, RegisterSerializer

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

    @staticmethod
    def register(request):

        if request.user.is_authenticated:
            return redirect('hello')

        if request.method == "POST":

            errors = []
            if request.user.username != request.POST['username']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    if user:
                        email_exists = "Email already exists"
                        errors.append(email_exists)
                except User.DoesNotExist:
                    pass
            if request.user.username != request.POST['username']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    if user:
                        username_exists = "Username already exists"
                        errors.append(username_exists)
                except User.DoesNotExist:
                    pass
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
            if request.POST['email'] == "":
                no_email = "You must enter an email"
                errors.append(no_email)
            if request.POST['username'] == "":
                no_username = "You must enter a username"
                errors.append(no_username)
            if request.POST['first_name'] != "":
                if request.POST['first_name'][0].isupper() == False:
                    name_not_capitalized = "Name must be capitalized"
                    errors.append(name_not_capitalized)
            if request.POST['last_name'] != "":
                if request.POST['last_name'][0].isupper() == False:
                    surname_not_capitalized = "Surname must be capitalized"
                    errors.append(surname_not_capitalized)
            form = NewUserForm(request.POST)

            are_errors = False

            if len(errors) > 0:
                are_errors = True

                return render(request, 'signup.html', {
                    'register_form':form ,
                    'errors': errors,
                    'are_errors': are_errors
                    })
            else:
                user = form.save()
                Token.objects.create(user=user)
                login(request, user)
                return redirect("hello")

        else:
            form = NewUserForm()
            return render(request, 'signup.html', {'register_form': form})


class SignInView(APIView):

 
    @staticmethod     
    def sing_in(request):

        if request.user.is_authenticated:
            return redirect('hello')

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
                Token.objects.update_or_create(user=user)
                login(request, user)
                return redirect('hello')

    @staticmethod
    def hello(request):
        return render(request, 'hello.html', {
                'username' : request.user
            })

    @staticmethod
    def sign_out(request):
       logout(request)
       return redirect('signin')

class EditUserView(APIView):

    @staticmethod
    def edit(request):

        if request.method == "POST":

            errors = []

            if request.user.email != request.POST['email']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    if user:
                        email_exists = "Email already exists"
                        errors.append(email_exists)
                except User.DoesNotExist:
                    pass
            if request.user.username != request.POST['username']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    if user:
                        username_exists = "Username already exists"
                        errors.append(username_exists)
                except User.DoesNotExist:
                    pass
            try:
                account = SocialAccount.objects.get(user=request.user)

                if request.user.email == account.user.email and request.POST['email'] != request.user.email:
                    change_email = "You can't change your email"
                    errors.append(change_email)
            except:
                pass

            if request.POST['email'] == "":
                no_email = "You must enter an email"
                errors.append(no_email)
            if request.POST['username'] == "":
                no_username = "You must enter a username"
                errors.append(no_username)
            if request.POST['first_name'] != "":
                if request.POST['first_name'][0].isupper() == False:
                    name_not_capitalized = "Name must be capitalized"
                    errors.append(name_not_capitalized)
            if request.POST['last_name'] != "":
                if request.POST['last_name'][0].isupper() == False:
                    surname_not_capitalized = "Surname must be capitalized"
                    errors.append(surname_not_capitalized)

            are_errors = False

            form = UserEditForm(initial={'first_name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'email': request.user.email,
                                            'username': request.user.username})

            if len(errors) > 0:
                are_errors = True

                return render(request, 'profile.html', {
                    'register_form':form ,
                    'errors': errors,
                    'are_errors': are_errors
                    })

            else:
                user = request.user
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.username = request.POST['username']
                user.save()
                return redirect('hello')
        else:

            form = UserEditForm(initial={'first_name': request.user.first_name,
                                            'last_name': request.user.last_name,
                                            'email': request.user.email,
                                            'username': request.user.username})
            return render (request, "profile.html", {
                "register_form":form})

class DeleteUserView(APIView):

    @staticmethod
    def delete(request):
        user = request.user
        user.delete()
        return redirect('signin')


# API USER

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        errors = []

        if 'email' not in request.POST:
            return Response('Debes de ingresar un email', status=status.HTTP_400_BAD_REQUEST)
        if 'username' not in request.POST:
            return Response('Debes de ingresar un username', status=status.HTTP_400_BAD_REQUEST)
        if 'password' not in request.POST:
            return Response('Debes de ingresar un password', status=status.HTTP_400_BAD_REQUEST)
        if 'first_name' not in request.POST:
            return Response('Debes de ingresar un nombre', status=status.HTTP_400_BAD_REQUEST)
        if 'last_name' not in request.POST:
            return Response('Debes de ingresar un apellido', status=status.HTTP_400_BAD_REQUEST)

        if request.POST['email'] == "":
            no_email = "You must enter an email"
            errors.append(no_email)
        if request.POST['username'] == "":
            no_username = "You must enter a username"
            errors.append(no_username)
        if request.POST['first_name'] != "":
            if request.POST['first_name'][0].isupper() == False:
                name_not_capitalized = "Name must be capitalized"
                errors.append(name_not_capitalized)
        if request.POST['last_name'] != "":
            if request.POST['last_name'][0].isupper() == False:
                surname_not_capitalized = "Surname must be capitalized"
                errors.append(surname_not_capitalized)

        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": Token.objects.create(user=user).key
        })


class EditUserApi(APIView):

    @staticmethod
    def put(request):

        try:
            user = request.POST['username']
            token = request.POST['token']
        except MultiValueDictKeyError:
            return Response("You must enter a username and a token", status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=user).first()

        if user is None:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        token_user = Token.objects.get(user=user)

        if token_user.key != token:
            return Response("You can't update this user.", status=status.HTTP_403_FORBIDDEN)


        new_first_name = request.POST['first_name'] if 'first_name' in request.POST else ""
        new_last_name = request.POST['last_name'] if 'last_name' in request.POST else ""

        errors = []

        if  new_first_name != "" :
            if not new_first_name[0].isupper():
                name_not_capitalized = "Name must be capitalized"
                errors.append(name_not_capitalized)
            else:
                user.first_name = new_first_name

        if new_last_name != "":
            if not new_last_name[0].isupper():
                surname_not_capitalized = "Surname must be capitalized"
                errors.append(surname_not_capitalized)
            else:
                user.last_name = new_last_name

        if len(errors) > 0:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


        user.save()

        return Response({
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username
        },
        "token": token_user.key,

        })

class DeleteUserApi(APIView):

    @staticmethod
    def delete(request, username=None):

        try:
            token = request.POST['token']
        except MultiValueDictKeyError:
            return Response("You must enter a token", status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=username)

        if user is None:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        token_user = Token.objects.get(user=user)

        if token_user.key != token:
            return Response("You can't update this user.", status=status.HTTP_403_FORBIDDEN)

        user.delete()

        return Response("User deleted", status=status.HTTP_200_OK)


class LoginApi(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'expiry': timezone.now() + timezone.timedelta(days=1),
        })