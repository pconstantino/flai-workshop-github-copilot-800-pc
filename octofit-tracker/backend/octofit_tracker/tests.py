from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team='Test Team'
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.team, 'Test Team')
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test User')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
    
    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='test@example.com',
            activity_type='Running',
            duration=30,
            calories=300,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.user_email, 'test@example.com')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='API Test User',
            email='apitest@example.com',
            team='Team Marvel'
        )
    
    def test_get_users_list(self):
        """Test retrieving list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list')
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'team': 'Team DC'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
    
    def test_get_users_by_team(self):
        """Test filtering users by team"""
        url = reverse('user-by-team')
        response = self.client.get(url, {'team': 'Team Marvel'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Test Team API',
            description='API Test Team'
        )
    
    def test_get_teams_list(self):
        """Test retrieving list of teams"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_team(self):
        """Test creating a new team"""
        url = reverse('team-list')
        data = {
            'name': 'New Team',
            'description': 'A brand new team'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='Activity Test User',
            email='activitytest@example.com',
            team='Team Marvel'
        )
        self.activity = Activity.objects.create(
            user_email=self.user.email,
            activity_type='Running',
            duration=45,
            calories=450,
            date=datetime.now()
        )
    
    def test_get_activities_list(self):
        """Test retrieving list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        url = reverse('activity-list')
        data = {
            'user_email': self.user.email,
            'activity_type': 'Cycling',
            'duration': 60,
            'calories': 600,
            'date': datetime.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)
    
    def test_get_activities_by_user(self):
        """Test filtering activities by user email"""
        url = reverse('activity-by-user')
        response = self.client.get(url, {'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_entry = Leaderboard.objects.create(
            user_email='leader@example.com',
            user_name='Leader User',
            team='Team Marvel',
            total_calories=5000,
            total_activities=10,
            rank=1
        )
    
    def test_get_leaderboard(self):
        """Test retrieving leaderboard"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_get_top_leaderboard(self):
        """Test getting top N from leaderboard"""
        url = reverse('leaderboard-top')
        response = self.client.get(url, {'limit': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='A test workout routine',
            activity_type='HIIT',
            duration=30,
            difficulty='Medium',
            calories_estimate=350
        )
    
    def test_get_workouts_list(self):
        """Test retrieving list of workouts"""
        url = reverse('workout-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        url = reverse('workout-list')
        data = {
            'name': 'New Workout',
            'description': 'A new workout routine',
            'activity_type': 'Running',
            'duration': 40,
            'difficulty': 'Easy',
            'calories_estimate': 300
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 2)
    
    def test_get_workouts_by_difficulty(self):
        """Test filtering workouts by difficulty"""
        url = reverse('workout-by-difficulty')
        response = self.client.get(url, {'difficulty': 'Medium'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
