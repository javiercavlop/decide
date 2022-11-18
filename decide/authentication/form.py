from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms    

from django.contrib.auth.forms import AuthenticationForm, UsernameField



class CustomAuthenticationForm(AuthenticationForm):

    username = UsernameField(

        label='Username or Email',

        widget=forms.TextInput(attrs={'autofocus': True})

    )
	
class NewUserForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	email = forms.EmailField(required=True)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class UserEditForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=30, required=True)
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	