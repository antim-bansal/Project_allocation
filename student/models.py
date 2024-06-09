from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.conf import settings # type: ignore


def upload_location(instance, filename):
    return "student_pdfs/{name}/{filename}".format(name=instance.name, filename=filename)


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True) 
    branch = models.CharField(max_length=50)
    cgpa = models.FloatField()
    resume_link = models.URLField(default='')  # Field to store the resume URL

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.username  # Set the student name as the username of the associated user
        super().save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message