"""The invite action handler"""
from .models import Invite
from ProjectPartnerManagement.models import ProjectPartner
from UserManagement.models import User
from Projects.models import Project

class InviteActionHandler():

    def __init__(self, invite, request_action):
        self.invite = invite
        self.request_action = request_action
        self.requires_action = False
        self.updated_action = ''
        self.updated_action_state = ''
        self.update_parameters = ['email', 'invite_status']
        self.registered_user = ''

    def handle_invite_actions(self):
        '''handles actions on an invite that require additional processing'''
        self.__infer_invite_actions()
        if self.updated_action == 'email':
            # send email to updated mail
            self.__send_email(self.updated_action_state)

        if self.updated_action == 'status':
            self.__handle_status_update()

    def __infer_invite_actions(self):
        '''infers from the request what type of processing needs to be done depending on the action'''
        param_map = {
            'email': 'email',
            'invite_status': 'status'
        }
        print(self.request_action.data)
        for param in self.update_parameters:
            if param in self.request_action.data: # check if parameters are part of the request
                self.updated_action = param_map[param]
                self.updated_action_state = self.request_action.data[param]
                break
            

    def __handle_status_update(self):
        '''
        handles status updates for the invites. Different statuses affect the app differently
        {
            0: 'PENDING',
            1: 'ACCEPTED',
            2: 'DECLINED',
            3: 'EXPIRED',
            4: 'CANCELLED'
        }
        '''

        if self.updated_action_state == 0:
            # still in pending state, do nothing
            pass

        if self.updated_action_state == 1:
            #accepted the invite
            return self.__handle_accept_invite()
            
        if self.updated_action_state == 2:
            # declined invite
            return self.__handle_rejected_invite()
        
        if self.updated_action_state == 3:
            # expired
            return self.__handle_expired_invite()

        if self.updated_action_state == 4:
            # cancelled
            return self.__handle_revoked_invite()

    def __check_user_isregistered(self):
        '''checks whether the invitee is registered. if not, we can ask them to register'''
        self.registered_user = User.objects.get(email = self.invite['email'])
        if self.registered_user:
            return True
        return False

    def __handle_accept_invite(self):
        '''handles accepted invite by invitee'''
        is_user = self.__check_user_isregistered()
        workspace_type = self.invite['workspace_type']
        if is_user == False:
            # handle registration
            pass
        if workspace_type.lower() == 'Project'.lower():
            return self.__add_to_project()
        
    async def __add_to_project(self):
        '''if the workspace is a project, adds the user to the project through project partners'''
        try:
            project = Project.objects.get(id=self.invite['invite_params']['id'])
            role = self.invite['invite_params']['role']
            if project.projectId:
                await ProjectPartner.objects.create(self.registered_user, project, role)
        except Exception as e:
            return e

    def __handle_rejected_invite(self):
        """
        when an invite is rejected:
        1. Send an email to the invitor telling them the invite is rejected
        2. Update the Invite status
        """

    def __contact_invitor(self):
        pass

    def __handle_revoked_invite(self):
        """
        Invite has been revoked by the invitor
        1. Contact recipient to update this;
        2. Update the invite status
        """
        pass


    def __handle_expired_invite(self):
        """
        Invite already expired;
        1. Contact recipient to update them
        2. Update the invite status to expired
        """
        pass

    def __send_email(self, recipient):
        """
        Helper method for sending emails - we ned to have more arguments; and work with templates
        """
        pass

    def handle_reminder(self):
        pass






