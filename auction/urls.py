from django.urls import path

from . import views

# URL Paths of the website are defined here
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('create', views.create, name='create')
]