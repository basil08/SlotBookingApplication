
from django.urls import path, include

from . import views

app_name = "authentication"

urlpatterns = [
  path('login', views.login, name='login'),
  path('logout', views.logoutUser, name='logout'),
  path('signup', views.signup, name='signup')
]