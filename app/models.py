
from django.db import models

from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth.models import User
from django import forms

import datetime
# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=150)


    def __str__(self):
        return f'{self.name}'


class SubCategory(models.Model):

    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Brand(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):

    Availability = (('In Stock', 'In Stock')), (('Out of Stock', 'Out of Stock'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    availability = models.CharField(choices=Availability, null=True, max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):

        return f'{self.name}'




class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists':'Email already exists.'})

    class Meta:
        model = User
        fields = ('username','email','password1','password2')


    def __init__(self, *args, **kwargs):

        super (UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'



    def save(self,commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_message['exists'])
        return self.cleaned_data['email']


class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image',default='')
    product = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    quantity = models.CharField(max_length=100, default=1)
    price = models.IntegerField(null=True)
    address = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15, default='')
    pincode = models.CharField(max_length=10)
    total = models.CharField(max_length=150)
    date = models.DateField(default=datetime.datetime.today)







class contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'