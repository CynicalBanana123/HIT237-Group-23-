"""
URL configuration for housingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path

# Optionally include API routes if REST framework is available
try:
    from tickets.api_views import TicketListAPIView  # noqa: E402
except Exception:
    TicketListAPIView = None

urlpatterns = [
    # Root and legacy /dashboard/ now handled by the `accounts` app (dashboard merged)
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('accounts.urls')),
    path('tickets/', include('tickets.urls')),
]

if TicketListAPIView is not None:
    urlpatterns += [
        path('api/tickets/', TicketListAPIView.as_view(), name='api_ticket_list'),
    ]
 
