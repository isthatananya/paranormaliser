from django.urls import path
from . import views

urlpatterns = [
    path('save_conversation/', views.save_conversation, name='save_conversation'),
    # path('get_conversation/<int:user_id>/', views.get_conversation, name='get_conversation'),
    # path('get_model_access_history/<int:user_id>/', views.get_model_access_history, name='get_model_access_history'),
]
