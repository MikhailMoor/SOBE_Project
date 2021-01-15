from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UserSignInForm, UserSignUpForm, UserKeycodeForm,ForgotPasswordForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.contrib.sessions.models import Session

from main.models import Sellers, SOBE_Users

def sign_up(request):
	error=0
	dict_error =""

	if request.method == "POST":
		form =  UserSignUpForm(data=request.POST)

		form_word = UserKeycodeForm(data=request.POST)
		
		first_name = request.POST.get("first_name")
		last_name = request.POST.get("last_name")
		password1 = request.POST.get("password1")
		password2 = request.POST.get("password2")

		key_answer = request.POST.get("key_answer")


		username = request.POST.get("username")
		email = request.POST.get("email")
		if User.objects.filter(email=email).exists():
			dict_error =dict()
			dict_error["email"] = []
			dict_error["email"].append("User with this mail already exists")

		elif User.objects.filter(username=username).exists():
			dict_error =dict()
			dict_error["username"] = []
			dict_error["username"].append("User with this name already exists")

		else:
			error = form.errors.as_json()
			if form.is_valid():
				ins = form.save()

				username = form.cleaned_data["username"]
				password = form.cleaned_data["password1"]

				user = authenticate(username=username, password=password1, email=email)
				ins.email = email
				ins.save()
				form.save_m2m()


				user = User.objects.get(username = username)
				record = SOBE_Users(avatar_image=None, balance=2000, account = user, key_answer=key_answer)
				record.save()



				sobe_user = None
				sobe_users = SOBE_Users.objects.all()
				for j in sobe_users:
					if j.account.id == user.id:
						sobe_user = j
						break


				record = Sellers(user=sobe_user)
				record.save()


				return redirect("sign_in")



			else:
				dict_error =dict()
				st="Enter a valid email address."
				if st in error:
					dict_error["email"] = []
					dict_error["email"].append(st)


				st = "The password is too similar to the username."
				if st in error:
					if not("password" in dict_error.keys()):
						dict_error["password"] = [st]
					else:
						dict_error["password"].append(st)


				st="This password is too short. It must contain at least 8 characters."
				if st in error:
					if not("password" in dict_error.keys()):
						dict_error["password"] = [st]
					else:
						dict_error["password"].append(st)



				st="This password is too common."
				if st in error:
					if not("password" in dict_error.keys()):
						dict_error["password"] = [st]
					else:
						dict_error["password"].append(st)

				st="This password is entirely numeric."
				if st in error:
					if not("password" in dict_error.keys()):
						dict_error["password"] = [st]
					else:
						dict_error["password"].append(st)


				st="The two password fields didn"
				new_st="The two password fields didn`t match."
				if st in error:
					if not("password"  in dict_error.keys()):
						dict_error["password"] = [new_st]
					else:
						dict_error["password"].append(new_st)








	form = UserSignUpForm()
	form_word =  UserKeycodeForm()
	data = {
		"form":form,
		"form_word":form_word,
		"error":dict_error
	}




	return render(request,"register/sign_up.html",data)


def sign_in(request):
	error=""
	request.session.clear()
	if request.method == "POST":
		form =  UserSignInForm(data=request.POST)
		if form.is_valid():

			email =  form.cleaned_data["email"]
			password =  form.cleaned_data["password1"]
			user = authenticate(username=email, password=password)
			if user is not None:
				username = user.username
				request.session["username"] = username
				return render(request,"main/index.html", {"username": username})
			else:
				error =  'Login Failed! Enter the username and password correctly'
        


	form = UserSignInForm()

	data = {
		"form":form,
		"error":error
	}

	return render(request,"register/sign_in.html",data)


def forgot_password(request):
	if request.method == "POST":
		email = request.POST.get("email")
		key_answer = request.POST.get("key_answer")



		user_all = User.objects.all()
		user = None
		for i in user_all:
			if i.email == email:
				user=i

		

		if user == None:
			message = "This email does not exist(("
			data = {
				"message":message
			}
			return render(request,"register/check_failed.html",data)



		sobe_user = SOBE_Users.objects.get(account=user)

		if sobe_user.key_answer==key_answer:
			request.session["email"] = email
			return redirect("check_complete")
		else:
			message = "Wrong secret keyword(("
			data = {
				"message":message
			}
			
			return render(request,"register/check_failed.html", data)


	form = ForgotPasswordForm()
	data = {
	"form":form
	}
	return render(request,"register/forgot_password.html",data)




def check_failed(request):
	message = "Hmmm ..."
	data = {
		"message":message
	}
	return render(request,"register/check_failed.html",data)


def check_complete(request):
	message = "Hmmm ..."
	data = {
		"message":message
	}
	if not request.session.get('email', None):
		return render(request,"register/check_failed.html", data)


	email= request.session["email"]
	if request.method == "POST":
		form = ChangePasswordForm(data=request.POST)
		password= request.POST.get("password1")
		
		user_all = User.objects.all()
		user = None
		for i in user_all:
			if i.email == email:
				user=i

		if user == None:
			message = "This email does not exist(("
			data = {
				"message":message
			}
			return render(request,"register/check_failed.html", data)

		user.set_password(password)
		user.save()
		return redirect("successful_change")

	form=ChangePasswordForm()
	data={
		"form":form
	}
	return render(request,"register/check_complete.html",data)


def successful_change(request):
	request.session.clear()
	return render(request,"register/successful_change.html")

def preload(request):
	return render(request,"register/preload.html")
