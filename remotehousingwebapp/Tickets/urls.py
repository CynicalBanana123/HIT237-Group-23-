from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.ticket_list, name='tickets'),
    path('user_ticket/', views.user_ticket, name='user_ticket'),
]