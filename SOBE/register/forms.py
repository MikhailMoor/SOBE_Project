from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()


class ChangePasswordForm(forms.Form):
	password1 = forms.CharField(required=True, label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})),
                                help_text=password_validation.password_validators_help_text_html())


class UserKeycodeForm(forms.Form):
	key_answer = forms.CharField(max_length=20, min_length=4, required=True, help_text='Required: Input keyword', widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Cyberpunk"}))


class ForgotPasswordForm(forms.Form):
	email = forms.CharField(max_length=50, required=True, help_text='Required: Input email',
	 widget=forms.TextInput(attrs={'class': "w-full px-3 py-2 text-sm leading-tight text-gray-700 border shadow appearance-none focus:outline-none focus:shadow-outline", 'placeholder':"Enter Email Address..."}))
	key_answer = forms.CharField(max_length=20, min_length=4, required=True, help_text='Required: Input keyword',
	 widget=forms.TextInput(attrs={'class': "w-full px-3 py-2 text-sm leading-tight text-gray-700 border shadow appearance-none focus:outline-none focus:shadow-outline", 'placeholder':"Enter your secret keyword..."}))


class UserSignUpForm(UserCreationForm):


	first_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: First Name', widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"John"}))
    
	last_name = forms.CharField(max_length=12, min_length=4, required=True, help_text='Required: Last Name', widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Doe"}))
    
	email = forms.EmailField(required=True, max_length=50, help_text='Required. Inform a valid email address.',
                             widget=(forms.TextInput(attrs={'placeholder':"john.doe@company.com", 'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})))
    
	password1 = forms.CharField(required=True, label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})),
                                help_text=password_validation.password_validators_help_text_html())

	password2 = forms.CharField(required=True,label=_('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"}),
                                help_text=_('Just Enter the same password, for confirmation'))

	username = forms.CharField(
		
        label=_('Username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': _("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})
    )

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ["username", "first_name", "last_name", "email", "password1", "password2"]






class UserSignInForm(forms.Form):

  
	email = forms.EmailField(required=True, max_length=50, help_text='Required. Inform a valid email address.',
                             widget=(forms.TextInput(attrs={'placeholder':"john.doe@company.com", 'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})))
    
	password1 = forms.CharField(required=True, label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})),
                                help_text=password_validation.password_validators_help_text_html())

	class Meta(UserCreationForm.Meta):
		model = User
		fields = ["email", "password1"]


