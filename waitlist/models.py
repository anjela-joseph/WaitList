from django.db import models
import uuid

class WaitlistEntry(models.Model):
    COURSE_CHOICES = [
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('executive', 'Executive'),
    ]

    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=20, choices=COURSE_CHOICES,default='student')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
