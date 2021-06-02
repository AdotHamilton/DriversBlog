from django.db import models
import re
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import CharField
from django.db.models.fields.reverse_related import ManyToManyRel

# Create your models here
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if (len(postData['user_name'])) < 3:
            errors['user_name'] = 'Username must be at least 3 characters!'
        if (len(postData['password'])) < 7:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Passwords must match!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        return errors

    def update_validator(self, postData):
        errors = {}
        if(len(postData['user_name'])) < 3:
            errors['user_name'] = 'Username must be at least 3 characters!'
        if (len(postData['password'])) < 7:
            errors['password'] = 'Password must be at least 8 characters'
        if postData['password'] != postData['confirmPW']:
            errors['password'] = "Passwords must match!"
        return errors

class ThreadManager(models.Manager):
    def thread_validator(self, postData):
        errors = {}
        if len(postData["title"]) < 3 or len(postData["title"]) > 50:
            errors["title"] = "Thread title must be 4-50 characters"
        




class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    pfp = models.ImageField(upload_to='img/', default='/img/pfp.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class VehicleManager(models.Manager):
    def vehicle_validator(self, postData):
        errors = {}
        if(postData["year"] < 1955 or postData["year"] > 2030):
            errors["year"] = "Vehicle year must be valid"
        if(len(postData["model"]) < 2 or len(postData["model"]) > 20):
            errors["model"] = "Vehicle model must be valid"
        if(len(postData["make"]) < 2 or len(postData["make"]) > 20):
            errors["make"] = "Vehicle make must be valid"

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    chassis = models.CharField(max_length=15, null=True)
    year = models.IntegerField()
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    owners = models.ManyToManyField(User, related_name="owned_vehicles")

class Thread(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    vehicle = models.ForeignKey(Vehicle, related_name="threads", on_delete=models.CASCADE, null=True )
    
    
class PostManager(models.Manager):
    def post_validator(self, postData):
        errors = {}
        if (len(postData["header"])) < 4 or len(postData["header"]) > 40:
            errors["header"] = "Header must be 4-40 characters"
        if (len(postData["content"])) > 260: 
            errors["content"] = "Please limit posts to 260 characters"
        if(len(postData["content"]) < 5):
            errors["content"] = "Body text must be 6 or more characters"
        return errors
        

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=40)
    img = models.ImageField(blank=True, upload_to="img/posts/")
    content = models.CharField(max_length=260)
    creator = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="users_liked")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", related_name="following", on_delete=models.CASCADE)

    following_user_id = models.ForeignKey("User", related_name="followers",  on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
