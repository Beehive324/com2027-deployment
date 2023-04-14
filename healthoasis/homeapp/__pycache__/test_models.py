from django.test import TestCase
from .models import User, UserReport, UserActivity, ExerciseType, Exercise, UserWorkouts, Workout, WorkoutExercises, UserLocation, Nutrition, WeekLog





class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
        email='testuser@example.com',
        username='testuser',
        password='password123',
        age=25,
        weight=70,
        height=175,
        gender='M',
        BMI=22,
        Location='New York'
    )
        self.exercise_type = ExerciseType.objects.create(
        name='Cardio',
        description='Exercises that increase heart rate and improve cardiovascular health.'
    )
        self.exercise = Exercise.objects.create(
        name='Running',
        description='A form of cardiovascular exercise that involves running at a steady pace.',
        type=self.exercise_type
    )
        self.workout = Workout.objects.create(
        name='Morning Cardio',
        description='A 30-minute cardio workout to start your day.',
    )
        self.workout_exercises = WorkoutExercises.objects.create(
        workout=self.workout,
        exercise=self.exercise,
        sets=3,
        reps=12,
        weight=0,
    )
        self.user_workouts = UserWorkouts.objects.create(
        user=self.user,
        workout=self.workout,
        date='2022-04-13',
        duration=30,
    )
        self.user_report = UserReport.objects.create(
        user=self.user,
        age=self.user.age,
        gender=self.user.gender,
    )
        self.user_activity = UserActivity.objects.create(
        user=self.user,
        is_active=True,
    )
        self.user_location = UserLocation.objects.create(
        user=self.user,
        city=self.user.Location,
        country='USA',
    )
        self.nutrition = Nutrition.objects.create(
        name='Grilled Chicken Salad',
        description='A salad made with grilled chicken, mixed greens, and other vegetables.',
        calories=300,
        protein=30,
        carbs=10,
        fat=20,
    )
        self.week_log = WeekLog.objects.create(
        user=self.user,
        week_number=1,
        workout=self.workout,
        date='2022-04-13',
        duration=30,
    )

def test_user_creation(self):
    self.assertEqual(self.user.email, 'testuser@example.com')
    self.assertEqual(self.user.username, 'testuser')
    self.assertEqual(self.user.age, 25)
    self.assertEqual(self.user.weight, 70)
    self.assertEqual(self.user.height, 175)
    self.assertEqual(self.user.gender, 'M')
    self.assertEqual(self.user.BMI, 22)
    self.assertEqual(self.user.Location, 'New York')

def test_exercise_type_creation(self):
    self.assertEqual(self.exercise_type.name, 'Cardio')
    self.assertEqual(self.exercise_type.description, 'Exercises that increase heart rate and improve cardiovascular health.')

def test_exercise_creation(self):
    self.assertEqual(self.exercise.name, 'Running')
    self.assertEqual(self.exercise.description, 'A form of cardiovascular exercise that involves running at a steady pace.')
    self.assertEqual(self.exercise.type, self.exercise_type)

def test_workout_creation(self):
    self.assertEqual(self.workout.name, 'Morning Cardio')
    self.assertEqual(self.workout.description, 'A 30-minute cardio workout to start your day.')

def test_workout_exercises_creation(self):
    self.assertEqual(self.workout_exercises.workout, self.workout)
    self.assertEqual(self.workout_exercises.exercise, self.exercise)
    
