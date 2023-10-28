from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from UserManagement.models import User



def default_json():
    return {
        'workspace_id': '', # can be a project, a module etc
        'invite_type': '',
        'role': '',
    }


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

# Create your models here.
class Invite(models.Model):
    """
    Invite Model for the Invite management app
    1. Works on how to invite new members into a project, whether they exist or not
    2. An invitee could be someone already registered to the application, or not
    3. An invitor could only be someone already registered to the application - and has sufficient permissions in that project to do so
    """

    INVITE_TYPE = {
        ('Project', 'Project')
    }

    INVITE_STATUS = {
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled')
    }

    id = models.AutoField(primary_key=True, editable=False, unique=True)
    email = models.EmailField()
    invite_type = models.CharField(choices=INVITE_TYPE, max_length=20)
    invite_params = models.JSONField(default=default_json)
    # invite_status = models.CharField(choices=INVITE_STATUS, max_length=10)
    invite_Status = models.IntegerChoices("Status", "PENDING ACCEPTED DECLINED EXPIRED CANCELED")
    email_sent = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    invite_host = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
        null=False,
        blank=False,
        related_name='invitor_user_id'
    )
    reminder = models.BooleanField(default=False)
    reminder_period = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(14)])
    invite_expiry = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    reminder_count = models.PositiveIntegerField(default=0)
    reminder_threshold = models.PositiveIntegerField(default=3,  validators=[MaxValueValidator(3)])


    def __str__(self):
        return f"""Invitee: {self.email} \n 
                        Invitor: {self.invite_host}
                        Status: {self.invite_Status}
                        email sent: {self.email_sent}
                        created on: {self.created_on}
                    """