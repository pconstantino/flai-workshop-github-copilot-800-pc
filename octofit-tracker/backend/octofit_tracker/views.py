from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, 
    TeamSerializer, 
    ActivitySerializer, 
    LeaderboardSerializer, 
    WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users.
    Provides CRUD operations for user management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users filtered by team name"""
        team = request.query_params.get('team', None)
        if team:
            users = User.objects.filter(team=team)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({"error": "Team parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams.
    Provides CRUD operations for team management.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        users = User.objects.filter(team=team.name)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get team statistics"""
        team = self.get_object()
        members = User.objects.filter(team=team.name)
        activities = Activity.objects.filter(user_email__in=[m.email for m in members])
        
        stats = {
            'team_name': team.name,
            'total_members': members.count(),
            'total_activities': activities.count(),
            'total_calories': sum(a.calories for a in activities),
        }
        return Response(stats)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for activities.
    Provides CRUD operations for activity logging.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities for a specific user by email"""
        email = request.query_params.get('email', None)
        if email:
            activities = Activity.objects.filter(user_email=email).order_by('-date')
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get activities filtered by activity type"""
        activity_type = request.query_params.get('type', None)
        if activity_type:
            activities = Activity.objects.filter(activity_type=activity_type).order_by('-date')
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({"error": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboard.
    Provides access to competitive rankings.
    """
    queryset = Leaderboard.objects.all().order_by('rank')
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N users from leaderboard"""
        limit = int(request.query_params.get('limit', 10))
        top_users = Leaderboard.objects.all().order_by('rank')[:limit]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard filtered by team"""
        team = request.query_params.get('team', None)
        if team:
            team_leaderboard = Leaderboard.objects.filter(team=team).order_by('rank')
            serializer = self.get_serializer(team_leaderboard, many=True)
            return Response(serializer.data)
        return Response({"error": "Team parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Refresh leaderboard based on current activities"""
        # Delete existing leaderboard entries
        Leaderboard.objects.all().delete()
        
        # Get all users
        users = User.objects.all()
        leaderboard_entries = []
        
        for user in users:
            user_activities = Activity.objects.filter(user_email=user.email)
            total_activities = user_activities.count()
            total_calories = sum(activity.calories for activity in user_activities)
            
            leaderboard_entries.append({
                'user_email': user.email,
                'user_name': user.name,
                'team': user.team,
                'total_calories': total_calories,
                'total_activities': total_activities,
            })
        
        # Sort by total calories and assign ranks
        leaderboard_entries.sort(key=lambda x: x['total_calories'], reverse=True)
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry['rank'] = rank
            Leaderboard.objects.create(**entry)
        
        # Return refreshed leaderboard
        refreshed_leaderboard = Leaderboard.objects.all().order_by('rank')
        serializer = self.get_serializer(refreshed_leaderboard, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for workout suggestions.
    Provides CRUD operations for personalized workout recommendations.
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get workouts filtered by activity type"""
        activity_type = request.query_params.get('type', None)
        if activity_type:
            workouts = Workout.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({"error": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty level"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({"error": "Difficulty parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get workout recommendations based on user's activity history"""
        email = request.query_params.get('email', None)
        if email:
            # Get user's most frequent activity type
            activities = Activity.objects.filter(user_email=email)
            if activities.exists():
                # Simple recommendation: suggest workouts of the user's favorite activity type
                activity_types = {}
                for activity in activities:
                    activity_types[activity.activity_type] = activity_types.get(activity.activity_type, 0) + 1
                favorite_type = max(activity_types, key=activity_types.get)
                workouts = Workout.objects.filter(activity_type=favorite_type)
            else:
                # No activity history, return easy workouts
                workouts = Workout.objects.filter(difficulty='Easy')
            
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
