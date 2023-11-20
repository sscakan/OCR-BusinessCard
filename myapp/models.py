from django.db import models

# Create your models here.
class Information(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.CharField(max_length=255,  unique=True)
    phone = models.CharField(max_length=355, unique=True)
    web  = models.CharField(max_length=255)
    mail = models.CharField(max_length=355)
    unclassified = models.CharField(max_length=355)
    
    def __str__(self):
        return self.company
    