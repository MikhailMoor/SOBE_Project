from django.shortcuts import render, redirect
from register.forms import UserSignInForm

from .models import Lots, Sellers, SOBE_Users, Categories, Regions, Image,Dealings, AvatarImage
from django.contrib.auth.models import User

from .forms import NewLotForm,ImageForm,AvatarImageForm, ChangeUsernameForm, UserKeycodeForm, EmailForm,ChangePasswordForm

import random
import datetime


from django.db.models import Q


def get_path_avatar(username):
	user_id = int(User.objects.get(username = username).id)
	
	user = None
	users = SOBE_Users.objects.all()
	for j in users:
		if j.account.id == user_id:
			user = j
			break

	if user == None:
		return None

	avatar_img_path = None

	avatar_img =  user.avatar_image
	if avatar_img!=None:
		avatar_img_path  = avatar_img.pic.url



	return avatar_img_path


def get_balance(username):
	user_id = int(User.objects.get(username = username).id)
	user = None
	users = SOBE_Users.objects.all()
	for j in users:
		if j.account.id == user_id:
			user = j
			break

	if user == None:
		return None

	return user.balance



def index(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")



	username = request.session["username"]


	avatar_img=get_path_avatar(username)

	balance = get_balance(username)

	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance
	}
	return render(request,"main/index.html", data)








def lots(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")


	q = request.GET.get("q")
	search_lots = []
	if q != None:
		q = q.lower()
		all_lots = Lots.objects.all()

		for i in all_lots:
			if q in i.name.lower():
				search_lots.append(i)
				continue
			if q in i.description.lower():
				search_lots.append(i)
				continue

			category = i.category.all()
			for j in category:
				j = str(j)
				if q in j.lower():
					search_lots.append(i)
					continue

			region = i.region.all()
			for j in region:
				j = str(j)
				if q in j.lower():
					search_lots.append(i)
					continue


	lots = []



	if  q != None:
		all_lots = search_lots
	else:
		all_lots = Lots.objects.all()

	for i in all_lots:
		if i.is_closed:
			continue
		name = i.name

		if len(i.description)>88:
			description = i.description[0:88] + "..."
		else:
			description = i.description

		price = i.price

		category = ""
		for j in i.category.all():
			category += f"#{j.name} "

		regions = ""
		for j in i.region.all():
			regions += f"#{j.name} "


		image = i.image.pic.url
		print(image)
		id_lots = i.id

		lots.append(
    			{
    			"name":name,
    			"description":description,
    			"price":price,
    			"category":category,
    			"image":image,
    			"id_lots":id_lots,
    			"regions":regions
    			}
    		)



	username = request.session["username"]
	balance = get_balance(username)
	avatar_img=get_path_avatar(username)

	data = {
	"username": username,
	"avatar_img":avatar_img,
	"lots":lots,
	"balance":balance
	}
	return render(request,"main/lots.html", data)


def full_lots(request, id_lots):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)



	lot = Lots.objects.get(id = int(id_lots))
	image = lot.image.pic.url

	name_lots = lot.name

	seller = lot.seller.user.account.username

	seller_id = lot.seller.user.account.id

	categories = ""
	for j in lot.category.all():
		categories += f"#{j.name} " 

	regions = "Regions: "
	for j in lot.region.all():
		regions += f"{j.name} "

	count = lot.count
	price = lot.price
	description = lot.description
	sel_avatar  = lot.seller.user.avatar_image
	sel_avatar_img = None
	if sel_avatar!= None:
		sel_avatar_img= sel_avatar.pic.path

	id_lots = lot.id

	is_closed = lot.is_closed
	data = {
			"username": username,

			"image":image,
			"sel_avatar_img":sel_avatar_img,
			"avatar_img":avatar_img,
			"name_lots":name_lots,
			"seller": seller,
			"seller_id":seller_id,
			"price":price,
			"description":description,
			"categories": categories,
			"regions": regions,
			"count":count,
			"id_lots":id_lots,
			"balance":balance,
			"is_closed":is_closed
			}

	return render(request,"main/full_lots.html", data)

def messager(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]

	avatar_img=get_path_avatar(username)
	balance = get_balance(username)
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance
	}
	return render(request,"main/messager.html", data)



def exchange_history(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]

	avatar_img=get_path_avatar(username)
	balance = get_balance(username)

	user_id = int(User.objects.get(username = username).id)
	user = None
	users = SOBE_Users.objects.all()
	for j in users:
		if j.account.id == user_id:
			user = j
			break


	dealings = []

	dealings_all = Dealings.objects.all()
	for i in dealings_all:
		if i.user == user:
			dealings.append([i.date,i.price,i.seller, i.lot])


	if len(dealings) == 0:
		dealings = None


	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"dealings":dealings
	}
	return render(request,"main/exchange_history.html", data)




def next(request,id_lots):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	balance = get_balance(username)
	avatar_img=get_path_avatar(username)
	message = None

	lot = Lots.objects.get(id = id_lots)

	user_id = int(User.objects.get(username = username).id)
	users = SOBE_Users.objects.all()
	user = None
	for j in users:
		if j.account.id == user_id:
			user = j
			break

	seller = lot.seller

	if seller.user == user:
		message = "You cannot exchange units for your lot!"

		data = {
		"username": username,
		"avatar_img":avatar_img,
		"id_lots":id_lots,
		"message":message,
		"balance":balance
		}
		return render(request,"main/next.html", data)


	balance = user.balance
	lot_price = lot.price

	if balance< lot_price:
		message = "You didn't have enough units to exchange!"

		data = {
		"username": username,
		"avatar_img":avatar_img,
		"id_lots":id_lots,
		"message":message,
		"balance":balance
		}
		return render(request,"main/next.html", data)

	if lot.count<=0:
		message = "Lot closed!"

		data = {
		"username": username,
		"avatar_img":avatar_img,
		"id_lots":id_lots,
		"message":message,
		"balance":balance
		}
		return render(request,"main/next.html", data)

	user.balance-=lot_price
	user.save()


	if lot.count == 1:
		lot.is_closed = True
		lot.num_reason_closing = 3
		lot.date_closed = datetime.datetime.today()



	lot.count -= 1
	lot.save()

	


	date = datetime.datetime.today()

	record = Dealings(date=date, price=lot_price, lot=lot, user=user, seller=seller)
	record.save()
	goodmessage = "Successful exchange!"


	data = {
		"username": username,
		"avatar_img":avatar_img,
		"id_lots":id_lots,
		"message":message,
		"goodmessage":goodmessage,
		"balance":int(user.balance)
		}
	return render(request,"main/next.html", data)
















def profile(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")

	
	username = request.session["username"]

	balance = get_balance(username)
	avatar_img=get_path_avatar(username)


	user = User.objects.get(username = username)

	name_user = f"{user.first_name} {user.last_name}"
	date, a, b = user.date_joined.isocalendar() 
	date %= 100


	user_id = int(User.objects.get(username = username).id)
	
	user_sobe = None
	users = SOBE_Users.objects.all()
	for j in users:
		if j.account.id == user_id:
			user_sobe = j
			break

	if user_sobe == None:
		return render(request,"register/not_logged.html")


	seller = None
	sellers = Sellers.objects.all()
	for j in sellers:
		if j.user.id == user_sobe.id:
			seller = j
			break

	if seller == None:
		data = {
		"username": username,
		"avatar_img":avatar_img,
		"name_user":name_user,
		"date":date,
		"lots":None,
		"balance":balance
		}
		return render(request,"main/profile.html", data)

	lots = []


	all_lots = []

	all_all_all_lots =  Lots.objects.all()
	for j in all_all_all_lots:
		if j.seller.id == int(seller.id):
			all_lots.append(j)


	for i in all_lots:
		if i.is_closed:
			continue
		name = i.name

		if len(i.description)>88:
			description = i.description[0:88] + "..."
		else:
			description = i.description

		price = i.price

		category = ""
		for j in i.category.all():
			category += f"#{j.name} "

		regions = ""
		for j in i.region.all():
			regions += f"#{j.name} "


		image = i.image.pic.url
		print(image)
		id_lots = i.id

		lots.append(
    			{
    			"name":name,
    			"description":description,
    			"price":price,
    			"category":category,
    			"image":image,
    			"id_lots":id_lots,
    			"regions":regions
    			}
    		)



	closed_lots = []
	all_lots = []

	all_all_all_lots =  Lots.objects.all()
	for j in all_all_all_lots:
		if j.seller.id == int(seller.id):
			all_lots.append(j)


	for i in all_lots:
		if not i.is_closed:
			continue
		name = i.name

		if len(i.description)>88:
			description = i.description[0:88] + "..."
		else:
			description = i.description

		price = i.price

		category = ""
		for j in i.category.all():
			category += f"#{j.name} "

		regions = ""
		for j in i.region.all():
			regions += f"#{j.name} "


		image = i.image.pic.url
		print(image)
		id_lots = i.id

		closed_lots.append(
    			{
    			"name":name,
    			"description":description,
    			"price":price,
    			"category":category,
    			"image":image,
    			"id_lots":id_lots,
    			"regions":regions
    			}
    		)

	if len(lots)==0:
		lots = None
	if len(closed_lots)==0:
		closed_lots = None

	data = {
	"username": username,
	"avatar_img":avatar_img,
	"name_user":name_user,
	"date":date,
	"lots":lots,
	"closed_lots":closed_lots,
	"balance":balance
	}
	return render(request,"main/profile.html", data)


def sign_out(request):
	request.session.clear()
	form = UserSignInForm()
	data = {
		"form":form
	}
	return render(request,"register/sign_in.html", data)



def add_lot(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	balance = get_balance(username)
	avatar_img=get_path_avatar(username)








	error=0
	dict_error =""

	if request.method == "POST":
		form =  NewLotForm(request.POST)
		
		name = request.POST.get("name")
		description = request.POST.get("description")
		count = request.POST.get("count")
		price = request.POST.get("price")
		category = request.POST.get("category")
		region = request.POST.get("region")


		if not count.isdigit():
			dict_error =dict()
			dict_error["count"] = []
			dict_error["count"].append("Wrong input")
		else:
			count = int(count)
			if count <= 0:
				dict_error =dict()
				dict_error["count"] = []
				dict_error["count"].append("Wrong input")

		if not price.replace('.','',1).isdigit():
			dict_error =dict()
			dict_error["price"] = []
			dict_error["price"].append("Wrong input")

		else:
			price = float(price)
			if price <= 0:
				dict_error =dict()
				dict_error["price"] = []
				dict_error["price"].append("Wrong input")

		if dict_error != "":
			form = NewLotForm()
			data = {
			"username": username,
			"avatar_img":avatar_img,
			"form":form,
			"error":dict_error,
			"balance":balance
			}
			return render(request,"main/add_lots.html", data)


		id_category = None
		categories = Categories.objects.all()
		for j in categories:
			if j.name == category:
				id_category = j.id


		if id_category == None:
			record = Categories(name=category)
			record.save()
		for j in categories:
			if str(j.name) == category:
				id_category = j.id


		id_region = None
		regions = Regions.objects.all()
		for j in regions:
			if j.name == region:
				id_region = j.id


		if id_region == None:
			record = Regions(name=region)
			record.save()
		for j in regions:
			if str(j.name) == region:
				id_region = j.id




		form2 = ImageForm(request.POST, request.FILES)


		

		personal = form2.save(commit=False)
		num = str(len(Image.objects.all()) + 1)
		personal.title = str(len(Image.objects.all()) + 1)
		personal.save()



		image_image =Image.objects.get(title = num)
		



		user_id = int(User.objects.get(username = username).id)
	
		user_sobe = None
		users = SOBE_Users.objects.all()
		for j in users:
			if j.account.id == user_id:
				user_sobe = j
				break

		if user_sobe == None:
			return None


		seller = None
		sellers = Sellers.objects.all()
		for j in sellers:
			if j.user.id == user_sobe.id:
				seller = j
				break


		record = Lots(name=name, description=description, count=count, price=price, date=datetime.datetime.now(), image=image_image,seller=seller)
		record.save()


		lot = Lots.objects.get(seller = seller, name = name)
		lot.category.add(Categories.objects.get(id=id_category))
		lot.region.add(Regions.objects.get(id=id_region))







		data = {
		"username": username,
		"avatar_img":avatar_img,
		"balance":balance
		}
		return render(request,"main/index.html", data)
	


	form = NewLotForm()
	form2 = ImageForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"form":form,
	"form2":form2,
	"error":dict_error,
	"balance":balance
	}
	return render(request,"main/add_lots.html", data)



def settings(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]

	avatar_img=get_path_avatar(username)
	balance = get_balance(username)
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance
	}
	return render(request,"main/settings.html", data)










def change_avatar_photo(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)


	if request.method == "POST":
		form = AvatarImageForm(request.POST, request.FILES)


		

		personal = form.save(commit=False)
		num = str(len(AvatarImage.objects.all()) + 1)
		personal.title = str(len(AvatarImage.objects.all()) + 1)
		personal.save()



		image_image = AvatarImage.objects.get(title = num)
		

		user_id = int(User.objects.get(username = username).id)
	
		user_sobe = None
		users = SOBE_Users.objects.all()
		for j in users:
			if j.account.id == user_id:
				user_sobe = j
				break

		
		user_sobe.avatar_image = image_image
		user_sobe.save()

		data = {
		"username": username,
		"avatar_img":image_image.pic.url,
		"balance":balance,
		}
		return render(request,"main/change_successfully.html", data)





	form=AvatarImageForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_avatar_photo.html", data)



def change_username(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)

	if request.method == "POST":
		form = ChangeUsernameForm(request.POST)

		new_username = request.POST.get("username")

		users_all = User.objects.all()
		user = None
		for i in users_all:
			if i.username == new_username:
				message = "A user with the same name already exists"
				data = {
				"username": username,
				"avatar_img":image_image.pic.url,
				"balance":balance,
				"message":message
				}
				return render(request,"main/change_failed.html", data)



			if i.username == username:
				user = i

		request.session["username"] = new_username
		user.username = new_username

		user.save()
		data = {
		"username": new_username,
		"avatar_img":avatar_img,
		"balance":balance,
		}
		return render(request,"main/change_successfully.html", data)


	form = ChangeUsernameForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_username.html", data)




def change_password_one(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)


	if request.method == "POST":
		key_answer = request.POST.get("key_answer")

		user_all = User.objects.all()
		user = None
		for i in user_all:
			if i.username == username:
				user=i


		sobe_user = SOBE_Users.objects.get(account=user)

		if sobe_user.key_answer==key_answer:
			request.session["change_password"] = True
			return redirect("change_password_two")
		else:
			message = "Wrong keyword"
			data = {
			"username": username,
			"avatar_img":avatar_img,
			"balance":balance,
			"message":message
			}
			return render(request,"main/change_failed.html", data)


	form = UserKeycodeForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_password_one.html", data)


def change_password_two(request):
	if not request.session.get('change_password', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)



	if request.method == "POST":
		if not request.session.get('username', None) or not request.session["change_password"]:
			message = "Hmm...."
			data = {
			"username": username,
			"avatar_img":avatar_img,
			"balance":balance,
			"message":message
			}
			return render(request,"main/change_failed.html", data)

		password = request.POST.get("password1")


		users_all = User.objects.all()
		user = None
		for i in users_all:
			if i.username == username:
				user = i

		user.set_password(password)
		user.save()

		data = {
		"username": username,
		"avatar_img":avatar_img,
		"balance":balance,
		}
		return render(request,"main/change_successfully.html", data)




	form = ChangePasswordForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_password_two.html", data)





















def change_email_address_one(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)


	if request.method == "POST":
		key_answer = request.POST.get("key_answer")

		user_all = User.objects.all()
		user = None
		for i in user_all:
			if i.username == username:
				user=i


		sobe_user = SOBE_Users.objects.get(account=user)

		if sobe_user.key_answer==key_answer:
			request.session["change_email"] = True
			return redirect("change_email_address_two")
		else:
			message = "A user with the same name already exists"
			data = {
			"username": username,
			"avatar_img":image_image.pic.url,
			"balance":balance,
			"message":message
			}
			return render(request,"main/change_failed.html", data)


	form = UserKeycodeForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_email_address_one.html", data)




def change_email_address_two(request):
	if not request.session.get('change_email', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)



	if request.method == "POST":
		if not request.session.get('username', None) or not request.session["change_email"]:
			message = "Hmm...."
			data = {
			"username": username,
			"avatar_img":image_image.pic.url,
			"balance":balance,
			"message":message
			}
			return render(request,"main/change_failed.html", data)

		email = request.POST.get("email")


		users_all = User.objects.all()
		user = None
		for i in users_all:
			if i.username == username:
				user = i

		user.email = email
		user.save()

		data = {
		"username": username,
		"avatar_img":avatar_img,
		"balance":balance,
		}
		return render(request,"main/change_successfully.html", data)









	form = EmailForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_email_address_two.html", data)












def change_first_name(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")

	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)

	if request.method == "POST":
		form = ChangeUsernameForm(request.POST)

		first_name = request.POST.get("username")
		users_all = User.objects.all()
		user = None
		for i in users_all:
			if i.username == username:
				user = i

		user.first_name = first_name
		user.save()

		data = {
		"username": username,
		"avatar_img":avatar_img,
		"balance":balance,
		}

		return render(request,"main/change_successfully.html", data)


	form = ChangeUsernameForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_first_name.html", data)



def change_last_name(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")

	username = request.session["username"]
	avatar_img=get_path_avatar(username)
	balance = get_balance(username)

	if request.method == "POST":
		form = ChangeUsernameForm(request.POST)

		last_name = request.POST.get("username")
		users_all = User.objects.all()
		user = None
		for i in users_all:
			if i.username == username:
				user = i

		user.last_name = last_name
		user.save()

		data = {
		"username": username,
		"avatar_img":avatar_img,
		"balance":balance,
		}

		return render(request,"main/change_successfully.html", data)


	form = ChangeUsernameForm()
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"form":form
	}
	return render(request,"main/change_last_name.html", data)




def change_successfully(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]

	avatar_img=get_path_avatar(username)
	balance = get_balance(username)
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance
	}
	return render(request,"main/change_successfully.html", data)


def change_failed(request):
	if not request.session.get('username', None):
		return render(request,"register/not_logged.html")
	username = request.session["username"]

	avatar_img=get_path_avatar(username)
	balance = get_balance(username)
	message = "Hmm..."
	data = {
	"username": username,
	"avatar_img":avatar_img,
	"balance":balance,
	"message":message
	}
	return render(request,"main/change_failed.html", data)