from django.urls import path
from app5 import views

app_name = "app5"

urlpatterns = [
    path('', views.index, name="index"),
    path('index/', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
]