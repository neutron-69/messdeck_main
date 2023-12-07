from django.db import models
from star_ratings.models import Rating

class Feedbacks(models.Model):
    user_name = models.CharField(max_length=100)
    feed_back = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to="feedback_pics/",blank=True) 

class total_daily(models.Model):
    date = models.DateField()
    breakfast = models.IntegerField(default=0)
    lunch = models.IntegerField(default=0)
    dinner = models.IntegerField(default=0)

class user_total(models.Model):
    user_name = models.CharField(max_length=100)
    breakfast = models.IntegerField(default=0)
    lunch = models.IntegerField(default=0)
    dinner = models.IntegerField(default=0)

class food_items(models.Model):
    food_item = models.CharField(max_length=100)
    def __str__(self):
        return self.food_item

class rating_model(models.Model):
    food_item = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class student_info(models.Model):
    user_name = models.CharField(max_length=100)
    student_bhawan = models.CharField(max_length=20)
    student_id = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    

    


