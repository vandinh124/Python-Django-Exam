from django.db import models
import re
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "First name cannot be empty"
        if len(post_data['last_name']) == 0:
            errors['last_name'] = "Last name cannot be empty"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid Email"
        
        if len(post_data['password']) < 8 :
            errors['password'] = "Password must be at least 8 characters"

        if post_data['password'] != post_data['password_confirmation']:
            errors['password_confirmation'] = "Password and Password Confirmation do not match"

        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = "Email already exists"
    
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        if len(User.objects.filter(email=post_data['login_email'])) == 0:
            errors['login_email'] = "Email not found"        
        return errors
    
    def edit_profile_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "First name cannot be empty"
        if len(post_data['last_name']) == 0:
            errors['last_name'] = "Last name cannot be empty"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid Email"
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = "Email already exists"
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, post_data):
        errors = {}
        if len(post_data['author']) <3:
            errors['author'] = "Author name must be at least 3 characters"
        if len(post_data['quote_message']) <10:
            errors['quote_message'] = "Quote must be at least 10 charaters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 

class Quote(models.Model):    
    author = models.CharField(max_length=45)
    quote_message = models.TextField(max_length=500)
    posted_by = models.ForeignKey(User, related_name= "user_posts", on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name= "user_favorites", on_delete = models.CASCADE)
    quote = models.ForeignKey(Quote, related_name = "quote_favorites", on_delete = models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
