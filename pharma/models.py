from email.policy import default

from django.db import models
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver


class help(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    def __str__(self):
        return f"{self.name} : {self.email} : {self.phone} : {self.message}"

class Seller(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='seller/images/', validators=[FileExtensionValidator(['jpg', 'png'])])
    documents = models.FileField(upload_to='seller/documents/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])])
    def __str__(self):
        return f"{self.user} "

class Categories(models.Model):
    category = models.CharField(max_length =100)
    image = models.ImageField(upload_to='pharma/images/', validators=[FileExtensionValidator(['jpg', 'png'])])
    def __str__(self):
        return f"{self.category}"

class Pharma(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    categor = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1, verbose_name="Category")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pharma/images/', validators=[FileExtensionValidator(['jpg', 'png'])])
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    Approval = models.BooleanField(default=False)
    shipping = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user}: {self.name} product"

class buyerinfo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    method = models.ForeignKey('paymentmethod', on_delete=models.CASCADE, null=True, verbose_name="Payment Method")
    def __str__(self):
        return f"{self.user}: {self.name} info"

class cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.ForeignKey(Pharma, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.user}: {self.name} cart"
class boughtitem(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    users = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    total_earned = models.IntegerField(default=0)
    order_id = models.CharField(max_length=100)
    buyer_info = models.ForeignKey(buyerinfo, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.email}: {self.buyer_info} bought item"

class bought(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.ForeignKey(cart, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user}:  items bought"
    
class popular(models.Model):
    name = models.ForeignKey(Pharma, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}: {self.views}views"
class Approval(models.Model):
    name = models.ForeignKey(Pharma, on_delete=models.CASCADE)
    approval = models.BooleanField(null=True)
    def __str__(self):
        return f"{self.name}: {self.approval}"

class paymentmethod(models.Model):
    method = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.method}"

class Payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., 'pending', 'success', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"

class Pending_payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., 'pending', 'success', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"



@receiver(post_delete, sender=Pharma)
def delete_video_on_model_delete(sender,instance,**kwargs):
      if instance.image:
          instance.image.delete(save=False)

