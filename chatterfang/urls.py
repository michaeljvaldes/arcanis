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
from rest_framework_nested import routers

from playgroups import views

router = routers.SimpleRouter()
router.register(r'playgroups', views.PlaygroupViewSet)

playgroups_router = routers.NestedSimpleRouter(
    router, r'playgroups', lookup='playgroup')
playgroups_router.register(
    r'players', views.PlayerViewSet, basename='playgroup-players')
playgroups_router.register(
    r'matches', views.MatchViewSet, basename='playgroup-matches')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'login/', views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path(r'', include(router.urls)),
    path(r'', include(playgroups_router.urls)),
    path('commanders/', views.CommanderList.as_view()),
    path('commanders/<str:pk>', views.CommanderDetail.as_view())
]
