from dateutil.relativedelta import relativedelta
from django.db import models

from core.helpers.model_currency_choices import CURRENCY_CHOICES


# Create your models here.
class Project(models.Model):
    '''Projects model for the project management app'''
    PROJECT_STATUS_CHOICES = [
        ('To-do', 'To-Do'),
        ('progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('on hold', 'Paused'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ]
    PROJECT_PRIORITY_CHOICES = [
        ('Critical', 'critical'),
        ('High', 'High priority'), 
        ('medium', 'Medium priority'),
        ('low', 'Low Priority')
    ]
    PROJECT_CURRENCIES = CURRENCY_CHOICES
    # required fields
    projectId = models.AutoField(primary_key=True, editable=False, unique=True)
    name= models.CharField(max_length=256)
    objective = models.TextField(max_length=1024)
    description = models.TextField(max_length=2048)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    estimated_cost = models.IntegerField()
    priority = models.CharField(choices=PROJECT_PRIORITY_CHOICES, max_length=10)
    # default fields
    project_currency = models.CharField(choices=PROJECT_CURRENCIES, default='KES', max_length=10)
    status = models.CharField(choices=PROJECT_STATUS_CHOICES, max_length=10, default='To-do')
    progress = models.FloatField(default=0)
    budget = models.IntegerField(default=1)
    budget_allocated = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    objective_achieved = models.BooleanField(default=False)
    # nullable and blanks
    estimated_start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    estimated_end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    estimated_timeline = models.CharField(null=True, blank=True, max_length=256)
    estimated_income = models.IntegerField(null=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    actual_cost = models.IntegerField(blank=True, null=True)
    actual_income = models.IntegerField(blank=True, null=True)
    cancel_reason = models.TextField(blank=True, null=True, max_length=2048)
    blocked_reason = models.TextField(blank=True, null=True, max_length=2048)
    review = models.TextField(blank=True, null=True, max_length=2048)



    def __str__(self):
        return f'''Name: {self.name} \n
                     Description: {self.description} \n 
                     Timeline: {self.estimated_timeline} \n
                     Start Date: {self.start_date} \n
                     Estimated cost: {self.estimated_cost} \n
                     Estimated income: {self.estimated_income} \n
                     Budget allocated: {self.budget_allocated}'''
    

    def save(self, *args, **kwargs):
        duration = relativedelta(self.estimated_end_date, self.estimated_start_date)
        self.estimated_timeline = self.format_duration(duration)
        super(Project, self).save(*args, **kwargs)

    def format_duration(self, duration):
        if duration.years >= 1:
            timeline = f"{duration.years} year(s), {duration.months} month(s)"
        elif duration.months >= 1:
            timeline = f"{duration.months} month(s), {duration.weeks} week(s)"
        elif duration.weeks >= 1:
            timeline = f"{duration.weeks} month(s), {duration.days} day(s)"
        else:
            timeline = f"{duration.days} day(s)"

        return timeline



