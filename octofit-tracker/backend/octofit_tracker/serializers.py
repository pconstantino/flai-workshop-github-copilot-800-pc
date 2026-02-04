from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'team', 'created_at']
        read_only_fields = ['_id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id') and instance._id:
            representation['_id'] = str(instance._id)
        return representation


class TeamSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at', 'member_count']
        read_only_fields = ['_id', 'created_at']
    
    def get_member_count(self, obj):
        """Get the count of users in this team"""
        return User.objects.filter(team=obj.name).count()
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id') and instance._id:
            representation['_id'] = str(instance._id)
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['_id', 'user_email', 'activity_type', 'duration', 'calories', 'date', 'created_at']
        read_only_fields = ['_id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id') and instance._id:
            representation['_id'] = str(instance._id)
        return representation


class LeaderboardSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_email', 'user_name', 'team', 'total_calories', 'total_activities', 'rank', 'updated_at']
        read_only_fields = ['_id', 'updated_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id') and instance._id:
            representation['_id'] = str(instance._id)
        return representation


class WorkoutSerializer(serializers.ModelSerializer):
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'activity_type', 'duration', 'difficulty', 'calories_estimate', 'created_at']
        read_only_fields = ['_id', 'created_at']
    
    def to_representation(self, instance):
        """Convert ObjectId to string for JSON serialization"""
        representation = super().to_representation(instance)
        if hasattr(instance, '_id') and instance._id:
            representation['_id'] = str(instance._id)
        return representation
