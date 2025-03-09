from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=False,default='')
    sub_category=models.ForeignKey(Sub_Category,on_delete=models.CASCADE,null=False,default='')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    image=models.ImageField(upload_to='ecommerce/ping')
    name=models.CharField(max_length=150)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='M')  # Add size field

    def __str__(self):
        return self.name

class UserCreateForm(UserCreationForm):
    email=forms.EmailField(required=True,label='Email',error_messages={'exists':'This Already Exists'})

    class Meta:
        model=User
        fields=('username','email','password1','password2')


    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
    
    def save(self,commit=True):
        user=super(UserCreateForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['emails'].error_message['exists'])
        return self.cleaned_data['email']
    

class Contact_us(models.Model):
    name=models.CharField(max_length=150)
    email=models.EmailField(max_length=150)
    subject=models.CharField(max_length=150)
    message=models.TextField()
    def __str__(self):
        return self.email
class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    size = models.CharField(max_length=3)  # Add size field
    total = models.CharField(max_length=1000, default='')
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)

    def __str__(self):
        return self.product

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=3)  # Add size field