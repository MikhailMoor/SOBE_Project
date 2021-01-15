
from django.urls import path, include
from . import views
from register import views as views_to
from django.conf.urls import url

urlpatterns = [
	
	path("index", views.index, name="index"),
	path("lots", views.lots, name="lots"),

	url(r'^$', views.lots, name="lots"),
	url(r'^lots/$', views.lots, name="lots"),
	url(r'^lots/(?P<id_lots>\d+)$', views.full_lots, name="full_lots"),
	url(r'^(?P<id_lots>\d+)$', views.full_lots, name="full_lots"),
	path("profile", views.profile, name="profile"),
	path("messager", views.messager, name="messager"),

	path("add_lot", views.add_lot, name="add_lot"),
	path("settings", views.settings, name="settings"),

	path("exchange_history", views.exchange_history, name="exchange_history"),

	path(r'^next/(?P<id_lots>\d+)$', views.next, name="next"),

	path("register/sign_in", views_to.sign_in, name="sign_in"),

	url(r'^lots/$', views.lots, name='lots'),





	path("change_avatar_photo", views.change_avatar_photo, name="change_avatar_photo"),
	path("change_username", views.change_username, name="change_username"),

	path("change_password_one", views.change_password_one, name="change_password_one"),
	path("change_password_two", views.change_password_two, name="change_password_two"),
	
	path("change_email_address_one", views.change_email_address_one, name="change_email_address_one"),
	path("change_email_address_two", views.change_email_address_two, name="change_email_address_two"),
	path("change_first_name", views.change_first_name, name="change_first_name"),
	path("change_last_name", views.change_last_name, name="change_last_name"),

	path("change_successfully", views.change_successfully, name="change_successfully"),
	path("change_failed", views.change_failed, name="change_failed"),
]
