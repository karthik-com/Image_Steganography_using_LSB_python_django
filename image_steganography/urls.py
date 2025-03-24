from django.urls import path
from .views import user_login, register, user_home, user_logout, encode_view, decode_view, home

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user_home/', user_home, name='user_home'),
    path('encode/', encode_view, name='encode_page'),
    path('decode/', decode_view, name='decode_page'),
]
