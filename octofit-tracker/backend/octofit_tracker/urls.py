"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
import os
from .views import (
    UserViewSet,
    TeamViewSet,
    ActivityViewSet,
    LeaderboardViewSet,
    WorkoutViewSet
)

# Create router and register viewsets
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

@api_view(['GET'])
def api_root(request, format=None):
    """
    API root endpoint that lists all available endpoints
    """
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'endpoints': {
            'users': f"{base_url}/api/users/",
            'teams': f"{base_url}/api/teams/",
            'activities': f"{base_url}/api/activities/",
            'leaderboard': f"{base_url}/api/leaderboard/",
            'workouts': f"{base_url}/api/workouts/",
            'admin': f"{base_url}/admin/",
        },
        'custom_endpoints': {
            'users_by_team': f"{base_url}/api/users/by_team/?team=<team_name>",
            'team_members': f"{base_url}/api/teams/<id>/members/",
            'team_stats': f"{base_url}/api/teams/<id>/stats/",
            'activities_by_user': f"{base_url}/api/activities/by_user/?email=<email>",
            'activities_by_type': f"{base_url}/api/activities/by_type/?type=<type>",
            'leaderboard_top': f"{base_url}/api/leaderboard/top/?limit=<n>",
            'leaderboard_by_team': f"{base_url}/api/leaderboard/by_team/?team=<team_name>",
            'leaderboard_refresh': f"{base_url}/api/leaderboard/refresh/",
            'workouts_by_type': f"{base_url}/api/workouts/by_type/?type=<type>",
            'workouts_by_difficulty': f"{base_url}/api/workouts/by_difficulty/?difficulty=<difficulty>",
            'workouts_recommended': f"{base_url}/api/workouts/recommended/?email=<email>",
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root-alternate'),
    path('api/', include(router.urls)),
]
