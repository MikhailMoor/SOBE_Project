from django.urls import path, include
from . import views

urlpatterns = [
	path("", views.sign_in, name="sign_in"),
	path("sign_in", views.sign_in, name="sign_in"),
	path("sign_up", views.sign_up, name="sign_up"),
	
	path("check_complete", views.check_complete, name="check_complete"),
	path("forgot_password", views.forgot_password, name="forgot_password"),
	path("preload", views.preload, name="preload"),
	path("check_failed", views.check_failed, name="check_failed"),
	path("successful_change", views.successful_change, name="successful_change"),
]
