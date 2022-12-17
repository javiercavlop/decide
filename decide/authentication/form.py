from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from postproc.models import UserProfile
from django import forms    

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import ugettext_lazy as _

class CustomAuthenticationForm(AuthenticationForm):

    username = UsernameField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

class LoginUserForm(AuthenticationForm):
	username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={
									'autofocus': True,
									'class':'form-control mb-lg-0 mb-2',
									}),
    )
	password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
										'class':'form-control mb-lg-0 mb-2',
										}),
    )
	
class NewUserForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(required=True)

	MALE = 'M'
	WOMEN = 'W'
	OTHER = 'O'

	genre_choices = ((MALE, 'Hombre'), (WOMEN, 'Mujer'), (OTHER, 'Otro'))

	genre = forms.ChoiceField(choices = genre_choices)
	
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password1', 'password2')

		widgets = {
			'username': forms.TextInput(attrs={'class':'form-control'}),
			'first_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			'email': forms.EmailInput(attrs={'class':'form-control'}),
			'password1': forms.TextInput(attrs={'class':'form-control'}),
			'password2': forms.TextInput(attrs={'class':'form-control'}),
			'genre': forms.Select(attrs={'class':'form-select'})
		}

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class UserEditForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(required=True)
	MALE = 'M'
	WOMEN = 'W'
	OTHER = 'O'

	genre_choices = ((MALE, 'Hombre'), (WOMEN, 'Mujer'), (OTHER, 'Otro'))

	genre = forms.ChoiceField(choices = genre_choices)
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email','genre')
		##widgets = {'username':forms.TextInput(attrs={'class'}),'first_name':forms.TextInput,'last_name':forms.TextInput,'email':forms.TextInput}

	