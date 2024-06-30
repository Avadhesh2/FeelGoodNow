from django.contrib.auth.models import User
from django.db import models


from django.db import models


class IdealData(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField()
    weight = models.FloatField()
    sleeping_hours = models.FloatField()
    bmi = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"IdealData - Age: {self.age}, Gender: {self.get_gender_display()}, Height: {self.height}, Weight: {self.weight}, Sleeping Hours: {self.sleeping_hours}, BMI: {self.bmi}"

    def save(self, *args, **kwargs):
        # Calculate BMI before saving
        self.bmi = self.calculate_bmi()
        super().save(*args, **kwargs)

    def calculate_bmi(self):
        try:
            return self.weight / (self.height * self.height)
        except ZeroDivisionError:
            return None


class UserData(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    weight = models.FloatField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField()
    activity_level = models.CharField(max_length=20, choices=[
        ('Light', 'Light Activity'),
        ('Moderate', 'Moderate Activity'),
        ('Heavy', 'Heavy Activity')
    ])
    sleeping_hours = models.FloatField()
    age = models.IntegerField()

    def __str__(self):
        return f"UserData - Weight: {self.weight}, Gender: {self.get_gender_display()}, Height: {self.height}, Activity Level: {self.activity_level}, Sleeping Hours: {self.sleeping_hours}, Age: {self.age}"


class Exercise(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Exercise - Age: {self.age}, Gender: {self.get_gender_display()}, Name: {self.name}"


class Food(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Food - Age: {self.age}, Gender: {self.get_gender_display()}, Name: {self.name}"


# youtube Video


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField('Video', related_name='users_favorite')

    def _str_(self):
        return self.user.username


class Video(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='videos', blank=True, null=True)
    video_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    thumbnail = models.URLField()
    url = models.URLField(blank=True, null=True)

    def _str_(self):
        return self.title
