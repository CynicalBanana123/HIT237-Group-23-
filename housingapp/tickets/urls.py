from django.urls import path
from django.views.generic import RedirectView
from . import views


app_name = 'tickets'

urlpatterns = [
    path(
        '',
        RedirectView.as_view(pattern_name='accounts:home', permanent=False),
        name='list'
    ),
    path('create/', views.TicketCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.TicketUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TicketDeleteView.as_view(), name='delete'),
    path('<int:pk>/close/', views.close_ticket, name='close'),
]

