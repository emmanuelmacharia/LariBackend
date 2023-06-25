from django.db import models

# Create your models here.
class Project(models.Model):
    '''Projects model for the project management app'''
    PROJECT_STATUS_CHOICES = [
        ('To-do', 'To-Do'),
        ('progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ]
    PROJECT_PRIORITY_CHOICES = [
        ('Critical', 'critical'),
        ('High', 'High priority'), 
        ('medium', 'Medium priority'),
        ('low', 'Low Priority')
    ]
    projectId = models.AutoField(primary_key=True, editable=False, unique=True)
    name= models.CharField(max_length=256)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    estimated_timeline = models.DurationField()
    estimated_cost = models.IntegerField()
    estimated_income = models.IntegerField(null=True)
    estimated_start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    status = models.CharField(choices=PROJECT_STATUS_CHOICES, max_length=10)
    priority = models.CharField(choices=PROJECT_PRIORITY_CHOICES, max_length=10)



