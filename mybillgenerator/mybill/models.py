from django.db import models
from django.contrib.auth.models import  User

# Create your models here.

class Registration(models.Model):
    Name = models.CharField(max_length=200)
    Address = models.TextField()
    Phone = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Password = models.CharField(max_length=200)
    Registration_date = models.DateField()
    User_role = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Buildings(models.Model):
    Building_name = models.CharField(max_length=200)
    Building_number = models.IntegerField()
    State = models.CharField(max_length=200)
    District = models.CharField(max_length=200)
    Place = models.CharField(max_length=200)
    Pin_code = models.IntegerField(default=0)
    Purpose = models.CharField(max_length=200)
    Phase = models.CharField(max_length=200)
    Tarif = models.CharField(max_length=200)
    Reg_Date = models.DateField(default=0)
    buil_reg = models.ForeignKey(Registration, on_delete=models.CASCADE)

class Readings(models.Model):
    Reading_date = models.DateField(default=0)
    Reading = models.IntegerField(default=0)
    r_reg = models.ForeignKey(Buildings, on_delete=models.CASCADE)

class Calculation(models.Model):
    Building_name = models.CharField(max_length=200)
    Building_number = models.IntegerField()
    Date_from = models.DateField(default=0)
    Previous_reading = models.IntegerField(default=0)
    Date_to = models.DateField(default=0)
    Current_reading = models.IntegerField(default=0)
    Amount = models.FloatField(default=0)
    Bill_date = models.DateField(default=0)
    Difference = models.FloatField(default=0)
    r_reg = models.ForeignKey(Buildings, on_delete=models.CASCADE)

class Feedback(models.Model):
    Name = models.CharField(max_length=200)
    Email = models.EmailField()
    Comment = models.TextField(max_length=200)
    status = models.TextField(max_length=200)

