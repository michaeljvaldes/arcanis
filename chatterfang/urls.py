"""
URL configuration for chatterfang project.

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
from django.urls import include, path
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

from playgroups import views

router = DefaultRouter()
router.register(r'matches', views.MatchViewSet, basename='match')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'login/', views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('playgroups/', views.PlaygroupList.as_view()),
    path('playgroups/<str:pk>/', views.PlaygroupDetail.as_view()),
    path('players/', views.PlayerList.as_view()),
    path('players/<str:pk>/', views.PlayerDetail.as_view()),
    path('commanders/', views.CommanderList.as_view()),
    path('commanders/<str:pk>', views.CommanderDetail.as_view()),
    path('', include(router.urls))
]
