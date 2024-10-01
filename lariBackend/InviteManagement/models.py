import datetime
from django.utils import timezone
import uuid
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

    WORKSPACE_TYPE = {
        ('Project', 'Project')
    }

    class InviteStatus(models.IntegerChoices):
        PENDING = 1, 'Pending'
        ACCEPTED = 2, 'Accepted'
        DECLINED = 3, 'Declined'
        EXPIRED = 4, 'Expired'
        CANCELLED = 5, 'Cancelled'

    INVITE_STATUS = {
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Expired', 'Expired'),
        ('Cancelled', 'Cancelled')
    }
    #uneditable fields
    id = models.AutoField(primary_key=True, editable=False, unique=True) #
    invite_uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)#
    email_sent = models.BooleanField(default=False)#
    created_on = models.DateTimeField(auto_now_add=True)#
    modified_on = models.DateTimeField(auto_now=True)#
    invite_host = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
        null=False,
        blank=False,
        # related_name='invitor_user_id'
    )#why would you want to update this?
    workspace_id = models.IntegerField(null=False, blank=False) # cant change unless you change the project

    # actionable changes
    email = models.EmailField() ## trigger a new email
    workspace_type = models.CharField(choices=WORKSPACE_TYPE, max_length=15) ## nothing? depends on the info on the email
    invite_status = models.IntegerField(choices=InviteStatus.choices, default=InviteStatus.PENDING)
    
    # non actionable changes
    invite_params = models.JSONField(default=default_json) ## nothing
    reminder = models.BooleanField(default=False) ## nothing
    reminder_period = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(14)]) ##nothing
    invite_expiry = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True) ## nothing
    reminder_count = models.PositiveIntegerField(default=0) ## nothing
    reminder_threshold = models.PositiveIntegerField(default=3,  validators=[MaxValueValidator(3)]) ## nothing


    def __str__(self):
        return f"""Invitee: {self.email} \n 
                        Invitor: {self.invite_host}
                        Status: {self.invite_status}
                        email sent: {self.email_sent}
                        created on: {self.created_on}
                    """
    
    def save(self, *args, **kwargs):
        '''adds expiry and status of the invite by default'''
        if not self.instance.pk:
            self.invite_expiry = timezone.now()  + datetime.timedelta(days=14)
            self.invite_status = 1
        super(Invite, self).save(*args, **kwargs)
