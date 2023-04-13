from django.db import models

# Create your models here.

class User(models.Model):
    email =  models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=10)
    bmi = models.FloatField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now_add=True)
    report_data = models.JSONField()

def __str__(self):
    return f"Report for {self.user.username} on {self.report_date}"



class UserActivity(models.Model):
    user = models.OneToOneFIeld(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - { 'Active' if self.active else 'Inactive'}"


class ExerciseType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserWorkouts(modes.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField()


    def __str__(self):
        return f"{self.user.username} - {self.workout.name} ({self.date})"


class Workout(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserNutrition(models.Model):
    name = models.CharField(max_length=50)
    calories = models.FloatField()