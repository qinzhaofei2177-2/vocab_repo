from django.urls import path

from . import views

#app_name = 'vocabexam'
urlpatterns = [
    path("", views.index, name='index'),
    path("exam", views.exam, name='exam'),
    path("register", views.register, name='register'),
    path("login", views.login_view, name='login'),
    path("loggingin", views.login_proc, name='loggingin'),
    path("logout", views.logout_proc, name='logout'),
    path("search", views.search, name='search'),
    path("search/<str:pattern>", views.search, name='search'),
    path("search/<str:pattern>/<int:limit>", views.search, name='search'),
]
