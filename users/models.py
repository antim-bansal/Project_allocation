from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_NONE = 'none'
    ROLE_STUDENT = 'student'
    ROLE_PROFESSOR = 'professor'
    ROLE_CHOICES = [
        #(ROLE_NONE, 'None'),
        (ROLE_STUDENT, 'Student'),
        (ROLE_PROFESSOR, 'Professor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_NONE)

