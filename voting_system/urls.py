"""
URL configuration for voting_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from core import views   # apna app import karo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='inedx'),   # index page
    path('admin-form/', views.admin_form, name='admin_form'),
    path('add-candidate/', views.add_candidate, name='add_candidate'),
    path('voter-form/', views.voter_form, name='voter_form'),
    path("voting/<str:unique_code>/", views.voting_page, name="voting_page"),
    path("time-limit/", views.time_limit, name="time_limit"),
    path("thank-you/", views.thank_you, name="thank_you"),

    
]
