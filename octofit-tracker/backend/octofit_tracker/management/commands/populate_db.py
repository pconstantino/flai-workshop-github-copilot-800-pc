from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing data...')
        
        # Delete all existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes fitness team'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League fitness warriors'
        )
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        marvel_heroes = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Steve Rogers', 'email': 'captainamerica@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Thor Odinson', 'email': 'thor@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Natasha Romanoff', 'email': 'blackwidow@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Bruce Banner', 'email': 'hulk@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Peter Parker', 'email': 'spiderman@marvel.com', 'team': 'Team Marvel'},
        ]
        
        dc_heroes = [
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'team': 'Team DC'},
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'team': 'Team DC'},
            {'name': 'Diana Prince', 'email': 'wonderwoman@dc.com', 'team': 'Team DC'},
            {'name': 'Barry Allen', 'email': 'flash@dc.com', 'team': 'Team DC'},
            {'name': 'Arthur Curry', 'email': 'aquaman@dc.com', 'team': 'Team DC'},
            {'name': 'Hal Jordan', 'email': 'greenlantern@dc.com', 'team': 'Team DC'},
        ]
        
        users_data = marvel_heroes + dc_heroes
        users = []
        for user_data in users_data:
            user = User.objects.create(**user_data)
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'HIIT']
        activities_created = 0
        
        for user in users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)  # 20-120 minutes
                calories = duration * random.randint(5, 12)  # Rough calorie estimate
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    date=activity_date
                )
                activities_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_created} activities'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        leaderboard_entries = []
        
        for user in users:
            # Calculate total activities and calories for each user
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
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries)} leaderboard entries'))
        
        # Create Workouts (suggestions)
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Avengers Assemble Cardio',
                'description': 'High-intensity cardio workout to channel your inner superhero',
                'activity_type': 'HIIT',
                'duration': 30,
                'difficulty': 'Hard',
                'calories_estimate': 350
            },
            {
                'name': 'Asgardian Strength Training',
                'description': 'Build strength worthy of Thor with this weightlifting routine',
                'activity_type': 'Weightlifting',
                'duration': 45,
                'difficulty': 'Hard',
                'calories_estimate': 400
            },
            {
                'name': 'Spider-Man Agility Run',
                'description': 'Quick and nimble running workout for enhanced agility',
                'activity_type': 'Running',
                'duration': 40,
                'difficulty': 'Medium',
                'calories_estimate': 320
            },
            {
                'name': 'Black Widow Combat Training',
                'description': 'Intense boxing and martial arts inspired workout',
                'activity_type': 'Boxing',
                'duration': 35,
                'difficulty': 'Hard',
                'calories_estimate': 380
            },
            {
                'name': 'Justice League Yoga Flow',
                'description': 'Find your inner peace and flexibility with this yoga session',
                'activity_type': 'Yoga',
                'duration': 50,
                'difficulty': 'Easy',
                'calories_estimate': 200
            },
            {
                'name': 'Flash Speed Cycling',
                'description': 'Lightning-fast cycling workout for speed demons',
                'activity_type': 'Cycling',
                'duration': 45,
                'difficulty': 'Medium',
                'calories_estimate': 380
            },
            {
                'name': 'Aquaman Aquatic Training',
                'description': 'Master the water with this comprehensive swimming workout',
                'activity_type': 'Swimming',
                'duration': 60,
                'difficulty': 'Medium',
                'calories_estimate': 450
            },
            {
                'name': 'Batman Night Patrol',
                'description': 'Dark Knight inspired endurance run for the vigilant',
                'activity_type': 'Running',
                'duration': 55,
                'difficulty': 'Hard',
                'calories_estimate': 500
            },
            {
                'name': 'Wonder Woman Warrior Workout',
                'description': 'Full-body HIIT workout for the modern warrior',
                'activity_type': 'HIIT',
                'duration': 40,
                'difficulty': 'Hard',
                'calories_estimate': 420
            },
            {
                'name': 'Superman Morning Flight',
                'description': 'Start your day with this energizing beginner cardio routine',
                'activity_type': 'Running',
                'duration': 25,
                'difficulty': 'Easy',
                'calories_estimate': 220
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout suggestions'))
        
        self.stdout.write(self.style.SUCCESS('\nDatabase population complete!'))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  - Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  - Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  - Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  - Leaderboard entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  - Workouts: {Workout.objects.count()}'))
