'''
Serializer for invite management. Handles the creation, updating, viewing and deletion of invites 
'''
import pytz
from   datetime import datetime
from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from UserManagement.models import User
from .models import Invite
from rest_framework.response import Response


from core.email_managent.send_email import *
from .invite_actions import InviteActionHandler


class InviteSerializer(serializers.ModelSerializer):
    '''serializer class for invite management'''
    class Meta:
        model = Invite
        fields = (
            'id', 'invite_uuid', 'email_sent', 'invite_host', 'workspace_id', 
            'email', 'workspace_type', 'invite_status', 'invite_params',
              'reminder', 'reminder_period', 'invite_expiry', 'reminder_count',
              'reminder_threshold' 
              )
        read_only_fields = ['id', 'invite_uuid', 'created_on']


    def validate(self, data):
        '''validates creation request data'''
        if not data['email']:
            raise serializers.ValidationError('invitee email is required')
        return data

    def create(self, validated_data):
        '''saves the new invite'''
        print('printed in create', validated_data)
        return Invite.objects.create(**validated_data)
    
    def send_invite(self, data):
        """sends the invite to the user"""
        pass

    def create_mail(self, data):
        relative_link = reverse('invite')

class UpdateInviteSerializer(serializers.ModelSerializer):
    '''handles updating invites (accepting and declining)'''

    class Meta:
        model = Invite
        fields = '__all__'
        read_only_fields = ['id', 'invite_uuid', 'created_on', 'invite_host', 'workspace_id', 'email', 'workspace_type']

    def validate_invite_details(self, invite):
        '''validates that the invite can be updated; return response object'''
        responseObj = {
            'is_valid': False,
            'message': 'Bad request',
            'requires_update': False,
            'update_actions': {
                'expired': False,
                'modified': False,
            },
        }
        expired = self.validate_invite_expiry(invite)
        if expired:
            # update request; return data to user
            responseObj['requires_update'] = True
            responseObj['update_actions']['expired'] = True
            responseObj['message'] = 'Invite has expired. Please request for a new one'
            return responseObj
        
        # check invite status isn't modified
        invite_status = invite['invite_status'].value
        if invite_status > 1:
            # if it isn't in pending state
            responseObj['update_actions']['modified'] = True
            responseObj['message'] = 'Cannot update an already modified invite. Please request for a new one'
            return responseObj

        responseObj['is_valid'] = True
        return responseObj

    def validate_invite_expiry(self, invite):
        '''checks the expiry of the invite; returns True if expired'''
        now = datetime.now(pytz.UTC)
        expiry_date = invite['invite_expiry'].value
        if invite['invite_status'] == 4:
            return True
        if now <=  datetime.fromisoformat(expiry_date.replace('Z', '+00:00')):
            return False
        return True
    
    def create_update_invite_status_object(self, request_action):
        '''creates the update object for updating the invite status''' 
        action = 1
        if request_action['expired']:
            action = 4
        return {'invite_status': action}


    def handle_invite_actions(self, invite_actions, request):
        '''handles the invite actions depending on the type of invites'''
        invite_handler = InviteActionHandler(invite_actions, request)
        invite_handler.handle_invite_actions()
