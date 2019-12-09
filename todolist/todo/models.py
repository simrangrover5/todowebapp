from django.db import models

# Create your models here.
class Myuser(models.Model):
    email = models.EmailField(unique=True,max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.email}"


class Mytasks(models.Model):
    user = models.ForeignKey(to=Myuser,on_delete=models.CASCADE)
    priority = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50)
    task = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user}"
