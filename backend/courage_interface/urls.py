from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("csrf/", views.get_csrf_token), 
]
