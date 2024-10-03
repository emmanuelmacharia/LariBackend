import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from .models import Invite
from .serializers import InviteSerializer, UpdateInviteSerializer
from core.helpers.auth_token_decorator import auth_token_validator


class CreateViewInvite(APIView):
    '''creates an invite'''
    serializer_class = InviteSerializer

    @auth_token_validator
    def post(self, request, format=None):
        '''creates the invite data'''
        user = request.user
        request.data['invite_host'] = user.userId
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        error_message = "Sorry, we cannot complete your request at the moment, please try again later"
        error_response = Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return error_response
        

    @auth_token_validator
    def get(self, request):
        '''gets all the invites a user has created'''
        user = request.user
        queryset = Invite.objects.filter(invite_host = user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FetchWorkspaceInvites(APIView):
    """fetches invite per invite type and Id"""
    serializer_class = InviteSerializer
    @auth_token_validator
    def get(self, id):
        workspace_id = id
        queryset = Invite.objects.filter(workspace_id = workspace_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetUpdateDeleteViewInvites(APIView):
    """fetches invite details"""
    serializer_class = UpdateInviteSerializer

    def fetch_from_db(self, id):
        '''fetches from db to stop repetition'''
        queryset = Invite.objects.get(invite_uuid = id)
        serializer = self.serializer_class(queryset)
        return serializer

    def get(self, request, uuid):
        '''gets a single invite by uuid'''
        serializer = self.fetch_from_db(uuid)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Invite not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid):
        "Accepts or rejects an invite"
        invite = self.fetch_from_db(uuid)
        validated_invite = self.serializer_class().validate_invite_details(invite)
        if not validated_invite['is_valid']:
            return self.handle_invalid_invite_updates(validated_invite, invite)
        return self.update_invite(invite, request)


    def handle_invalid_invite_updates(self, validated_invite, invite):
        if validated_invite['requires_update'] == True:
                update_action = validated_invite['update_actions']

                request = self.serializer_class().create_update_invite_status_object(update_action)
                saved_data = self.update_invite(invite, request)
                response = {
                    'message': validated_invite['message'],
                    'is_valid': validated_invite['is_valid'],
                    'status': validated_invite['update_actions']
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': validated_invite['message']}, status=status.HTTP_400_BAD_REQUEST)


    def update_invite(self, invite, request):
        request_data = request.data
        update_serializer = self.serializer_class(invite, data = request_data, partial=True)
        update_serializer.is_valid(raise_exception=True)
        import pdb; pdb.set_trace()
        try:
            update_serializer.save()
            print('we got here', update_serializer.data)
        except Exception as e:
            print('were in the exception now', e.__str__())
            return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        invite_action_data = update_serializer.data
        self.serializer_class().handle_invite_actions(invite_action_data, request)
        response =  {'status': True, 'data': update_serializer.data}
        return Response(response, status=status.HTTP_200_OK)


            
            




