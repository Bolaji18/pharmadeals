from email.policy import default

from django.db import models
import os
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete
from django.dispatch import receiver

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
    categor = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pharma/images/', validators=[FileExtensionValidator(['jpg', 'png'])])
    description = models.TextField()
    price = models.IntegerField()
    stock = models.IntegerField()
    def __str__(self):
        return f"{self.user}: {self.name} product"
class Approval(models.Model):
    name = models.ForeignKey(Pharma, on_delete=models.CASCADE)
    approval = models.BooleanField(null=True)
    def __str__(self):
        return f"{self.name}: {self.approval}"


@receiver(post_delete, sender=Pharma)
def delete_video_on_model_delete(sender,instance,**kwargs):
      if instance.image:
          instance.image.delete(save=False)

