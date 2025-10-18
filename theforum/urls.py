from django.contrib import admin
from django.urls import path, include
from . import views

app_name='theforum'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('', views.homepage, name="homepage"),
    path('f/<slug:slug>/', views.thread_view, name="thread"),
    path('post/<slug:slug>/', views.post_view, name="post"),
]