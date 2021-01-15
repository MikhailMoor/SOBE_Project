from django.db import models
from django.contrib.auth.models import User

class Regions(models.Model):
	name = models.CharField(max_length=200, help_text="Enter a lot region")

	def __str__(self):
		return self.name

class Categories(models.Model):
	name = models.CharField(max_length=200, help_text="Enter a lot category")

	def __str__(self):
		return self.name

class Image(models.Model):
	title = models.CharField(max_length=200)
	pic = models.ImageField(upload_to='lots_img/')
	def __str__(self):
		return self.title

class AvatarImage(models.Model):
	title = models.CharField(max_length=200)
	pic = models.ImageField(upload_to='avatar_img/')
	def __str__(self):
		return self.title


class Lots(models.Model):
	name = models.CharField(max_length=200, help_text="Enter lot name")
	description = models.TextField(max_length=1000, help_text="Enter lot description", blank=True)
	count = models.PositiveIntegerField(help_text="Enter lot count")
	price = models.FloatField(blank=True,help_text="Enter lot price")
	date = models.DateField(null=True, blank=True)
	seller = models.ForeignKey("Sellers", on_delete=models.CASCADE, null=True)
	category = models.ManyToManyField(Categories,help_text="Enter lot category")
	region = models.ManyToManyField(Regions,help_text="Enter lot region")
	image = models.OneToOneField(Image,on_delete=models.SET_NULL, null=True,help_text="Enter lot image")


	date_closed = models.DateField(null=True, blank=True, default=None)
	is_closed = models.BooleanField(null=True, blank=True, default=False)
	num_reason_closing = models.PositiveIntegerField(null=True, default=0)
	#причины закрытия:
	#0 - не закрыт
	#1 - закрыт досрочно владельцем
	#2 - закрыт досрочно админом
	#3 - закрыт т.к. кончилось кол-во
	def __str__(self):
		return self.name

class Sellers(models.Model):
	user = models.OneToOneField("SOBE_Users",on_delete=models.CASCADE,null=True)
	def __str__(self):
		return f"Seller {self.user.account.username}"



class SOBE_Users(models.Model):
	avatar_image = models.OneToOneField(AvatarImage,on_delete=models.SET_NULL,null=True)
	balance = models.IntegerField()
	account = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	key_answer = models.CharField(max_length=20)
	def __str__(self):
		if self.account!=None:
			return self.account.username
		else:
			return "New"





class Dealings(models.Model):
	date = models.DateField(null=True, blank=True)
	price = models.FloatField(blank=True)
	lot = models.ForeignKey(Lots, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(SOBE_Users, null=True, on_delete=models.SET_NULL)
	seller = models.ForeignKey(Sellers, null=True, on_delete=models.SET_NULL)