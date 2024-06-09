from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.conf import settings # type: ignore
from student.models import Student
from django.utils import timezone # type: ignore
from datetime import timedelta

class Professor(models.Model):
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'), 
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True) 
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    expertise = models.CharField(max_length=255)
    minimum_cgpa = models.FloatField(default=0.0)
    is_hod = models.BooleanField(default=False)
    selection_method = models.CharField(
        max_length=20,
        choices=[
            ('CGPA', 'CGPA Basis'),
            ('FCFS', 'First-Come, First-Served'),
        ],
        default='CGPA'
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    max_students = models.PositiveIntegerField(default=5)
    rem_students = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} -  {self.professor.name}"
    
class Allocation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True, blank=True)
    selected = models.BooleanField(default=False)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.IntegerField(default=0) 
    created_at = models.DateTimeField(default=timezone.now,null=True) 
    def __str__(self):
        return f"{self.student.name} -  {self.professor.name} - Priority: {self.priority}"

from django.utils import timezone
from datetime import timedelta
from django.db import models

class Deadline(models.Model):
    def default_deadline():
        return timezone.now() + timedelta(weeks=1)

    deadline = models.DateTimeField(default=default_deadline)

    def __str__(self):
        return f"{self.deadline}"

# from django.utils import timezone
# from datetime import timedelta

# class Deadline(models.Model):
#     def default_deadline():
#         return timezone.now().date() + timedelta(weeks=1)

#     deadline = models.DateField(default=default_deadline)

#     def __str__(self):
#         return f"{self.deadline}"



class SelectedStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    selection_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - Selected by {self.professor.name}"
    

# class DeadlineModel(models.Model):
    # deadline = models.DateTimeField()