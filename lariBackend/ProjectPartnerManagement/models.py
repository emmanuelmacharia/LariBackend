from django.db import models
from UserManagement.models import User
from Projects.models import Project

# Create your models here.
class ProjectPartner(models.Model):
    '''Junction table that relates the users and their projects'''
    PROJECT_ACCESS_LEVELS = [
        ('3', 'Owner'), # everything a partner does, but can also delete
        ('2', 'partner'), # can view and edit everything on the project
        ('1', 'collaborator'), # can only view and edit some aspects on the project
        ('0', 'view only access'), # only has view access rights
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project_partner_userid'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='project_partner_projectid'
    )
    user_access_level = models.IntegerField(choices=PROJECT_ACCESS_LEVELS, default=0)

