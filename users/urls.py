from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('', user_main, name='user_main'),
    path('signup/', user_signup, name='user_signup'),
    path('login/', user_login, name='user_login'),
]