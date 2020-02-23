from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

#User table
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #usertype = 0 for normal users,1 for chefs and 2 for restaurants,-1 for admin
    usertype=models.IntegerField(default=0) 
    address=models.CharField(max_length=300,blank=True)
    picture=models.ImageField(upload_to='profile_images',blank=True)
    def __str__(self):
        return self.user.username
    
#Recipe table
class Recipe(models.Model):
    recipe_id=models.AutoField(primary_key=True)
    recipe_name=models.CharField(max_length=128)
    username = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    #time taken in minutes
    time_taken = models.IntegerField()
    #level = 0 for beginner,1 for intermediate, 2 for expert
    level = models.IntegerField()
    #ingredients required seperated by a comma
    ingredients = models.TextField(max_length=500)
    #cooking type:0 for non-vegeterian,1 for vegetarian , 2 for vegan
    cooking_type = models.IntegerField(default=0)
    cuisine = models.CharField(max_length=128)
    image1 = models.ImageField(upload_to='recipe_images',blank=False)
    image2 = models.ImageField(upload_to='recipe_images',blank=True)
    image3 = models.ImageField(upload_to='recipe_images',blank=True)
    image4 = models.ImageField(upload_to='recipe_images',blank=True)
    image5 = models.ImageField(upload_to='recipe_images',blank=True)
    description = models.TextField(max_length=2000)
    created = models.DateTimeField(default=timezone.now())
    modified = models.DateTimeField()
    
    def save(self, *args,**kwargs):
        self.modified = timezone.now()
        super(Recipe,self).save(*args,**kwargs)
    #average rating
    @property
    def average_rating(self):
        total = 0
        count = Review.objects.filter(recipe_id=self.recipe_id).count()
        reviews = Review.objects.filter(recipe_id=self.recipe_id)
        for r in reviews:
            total+=r.rating
        return total/count
    def __str__(self):
        return self.recipe_id
        
        
    
 #Review table   
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    recipe_id=models.ForeignKey(Recipe,on_delete=models.CASCADE)
    username=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    description=models.TextField(max_length=500)
    created = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.review_id
    
#Reports table
class Report(models.Model):
    report_id=models.AutoField(primary_key=True)
    #posttype = 0 for recipe , 1 for review
    post_type=models.IntegerField()
    #if post type = 0 post_id = recipe_id elsepost_id = review_id
    post_id=models.IntegerField()
    username=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    #False = assigned, True=resolved
    status=models.BooleanField(default=False)
    action_taken=models.CharField(max_length=500,blank=True)
    created = models.DateTimeField(default=timezone.now())
    modified = models.DateTimeField()
    
    def save(self, *args,**kwargs):
        self.modified = timezone.now()
        super(Report,self).save(*args,**kwargs)
    def __str__(self):
        return self.review_id
    
    
    