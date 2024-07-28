from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

#UserProfile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(default="user.png",null=True,blank=True)
    
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    email_address =models.EmailField(null=True,blank=True)
    debt = models.IntegerField(null=True, blank=True,default=0)
    loyalty_points = models.FloatField(null=True, blank=True,default=0)
 

    def __str__(self):
        return str(self.first_name) +' '+ str(self.second_name)
    
    
class Product(models.Model):
    product_name= models.CharField(max_length=266)
    product_description = models.TextField(null=True)
    OTHER_UNITS = " "
    KILOGRAMS = "Kg"
    GRAMS = "g"
    UNITS_CHOICES = {
        OTHER_UNITS : " ",
        KILOGRAMS: "Kilograms",
        GRAMS: "Grams",
     }
    units = models.CharField(
    max_length= 10,
    choices=UNITS_CHOICES,
    default=OTHER_UNITS,
    )
    total_units = models.IntegerField(null=True)
    unit_buying_price= models.IntegerField(null=True)
    unit_selling_price= models.IntegerField(null=True)
    

    def __str__(self):
       return self.product_name

class Service(models.Model):
    service_name = models.CharField(max_length=266)
    service_description = models.CharField(max_length=266, null=True)
    service_price = models.IntegerField(null=True)
    

    def __str__(self):
       return self.service_name
    

class Sale(models.Model):
    customer_name = models.ForeignKey(Customer, on_delete = models.PROTECT)
    phone = models.CharField(max_length=12,null=True)
    services = models.CharField(max_length=255,default="" )
    CASH = "cash"
    MPESA = "Mpesa"
    PAYMENT_MODE = {
        CASH : "cash",
        MPESA : "Mpesa"
        }
    payment_mode = models.CharField(
    max_length= 10,
    choices=PAYMENT_MODE,
    default=CASH,
    )
    mpesa_code = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=40, decimal_places=2,default=0)
    date_paid = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return str(self.date_paid)
    
    class Meta:
        ordering:['-date_paid'] # type: ignore

class Booking(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    second_name = models.CharField(max_length=50, null=False)
    phone_number = models.IntegerField(null=False)
    book_date = models.CharField(max_length=50)
    book_time= models.CharField(max_length=50, default="", null=False)

    def __str__(self):
        return self.first_name

   
    
