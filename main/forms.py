from django import forms
from .models import Lots, Image , AvatarImage
from django.db import models
from django.contrib.auth import password_validation

from django.utils.translation import gettext_lazy as _


class NewLotForm(forms.ModelForm):


	name = forms.CharField(max_length=30, min_length=4, required=True, help_text='Enter lot name',
	 widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Name your lot"}))

	description = forms.CharField(help_text='Enter lot description',
	 widget=forms.Textarea(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Describe your lot"}))

	count = forms.IntegerField(help_text='Enter lot count',  required=True,
	 widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Count of your lot"}))


	price = forms.FloatField(help_text='Enter lot price',  required=True,
	 widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Price of your lot"}))

	category = forms.CharField(max_length=254, help_text='Enter lot category', required=True,
		widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Category of your lot"}))

	region = forms.CharField(max_length=254, help_text='Enter lot region', required=True,
		widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Region of your lot"}))




	#image = models.ImageField(help_text='Enter lot image',upload_to='main/static/main/lots_img')
	class Meta:

		model = Lots
		fields = ('name', 'description', 'count', 'price', 'category' , 'region')


class ImageForm(forms.ModelForm):
	title = forms.CharField(max_length=30, min_length=1, required=True, help_text='Enter lot name',
	 widget=forms.TextInput(attrs={'class': "block w-full p-3 my-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Name your img"}))

	class Meta:
		model = Image
		fields = ('title', 'pic')




class AvatarImageForm(forms.ModelForm):
	title = forms.CharField(max_length=30, min_length=1, required=True, 
	 widget=forms.TextInput(attrs={'class': "block w-full p-3 my-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Name your img"}))

	class Meta:
		model = AvatarImage
		fields = ('title', 'pic')





class ChangeUsernameForm(forms.Form):
	username = forms.CharField(max_length=150, min_length=1, required=True, 
	 widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})
    )


class ChangePasswordForm(forms.Form):
	password1 = forms.CharField(required=True, label=_('Password'),
                                widget=(forms.PasswordInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner"})),
                                help_text=password_validation.password_validators_help_text_html())


class UserKeycodeForm(forms.Form):
	key_answer = forms.CharField(max_length=20, min_length=4, required=True, help_text='Required: Input keyword', widget=forms.TextInput(attrs={'class': "block w-full p-3 mt-2 text-gray-700 bg-gray-200 appearance-none focus:outline-none focus:bg-gray-300 focus:shadow-inner", 'placeholder':"Cyberpunk"}))





class EmailForm(forms.Form):
	email = forms.CharField(max_length=50, required=True, help_text='Required: Input email',
	 widget=forms.TextInput(attrs={'class': "w-full px-3 py-2 text-sm leading-tight text-gray-700 border shadow appearance-none focus:outline-none focus:shadow-outline", 'placeholder':"Enter Email Address..."}))
	