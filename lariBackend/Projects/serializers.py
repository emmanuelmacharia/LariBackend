from rest_framework import serializers
from .models import Project
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class ProjectsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['projectId', 'created_on']
        
    def validate(self, data):
        """validates initial project data"""
        if not data.get('name') or not data.get('description') or not data.get('objective'):
            raise serializers.ValidationError("Name, description, or objective are required fields.")
        if not data.get('estimated_start_date') or not data.get('estimated_end_date'):
            raise serializers.ValidationError("Estimated start date or end date are required fields.")
        if not data.get('estimated_cost'):
            raise serializers.ValidationError("Estimated cost is a required field.")
        return data
    
    def create(self, validated_data):
        return Project.objects.create(**validated_data)
    

class ProjectUpdateSerializer(serializers.ModelSerializer):
    '''responsible for viewing, updating and deleting the projects and their details'''

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['projectId', 'created_on']
    
    def create_detailed_response(self, serialized_data, access_level):
        '''creates the response for getting the detailed project response'''
        response = serialized_data
        if access_level <= 1:
            modified_response = {
                "projectId": response["projectId"],
                "name": response["name"],
                "objective": response['objective'],
                "description": response['description'],
                "created_on": response['created_on'],
                "priority": response['priority'],
                "status": response['status'],
                "progress": response['progress'],
                "budget_allocated": response['budget_allocated'],
                "is_deleted": response['is_deleted'],
                "objective_achieved": response['objective_achieved'],
                "estimated_start_date": response['estimated_start_date'],
                "estimated_end_date": response['estimated_end_date'],
                "estimated_timeline": response['estimated_timeline'],
                "start_date": response['start_date'],
                "end_date": response['end_date'],
                "review": response['review']
            }
            response = modified_response
        return response
    

    def partner_only_update_fields(self):
        '''returns the fields that a only a partner or owner can update in a project'''
        return [
            'estimated_cost', 'project_currency', 'budget', 'budget_allocated',
            'objective_achieved', 'estimated_income', 'actual_cost', 'actual_income', 'priority'
        ]
    
    def validate_status_permutations(self, request_data, project, user_access):
        '''
        Checks for the specific rulesets pertaining to updating the status;
        including checking for roles, required fields for some statuses etc.
        '''
        # check for cancellation status
        if 'status' in request_data and request_data['status'].lower() == 'cancel':
            if user_access <= 1:
                return Response({ 'message': 'You do not have the permissions to cancel this project'}, status=status.HTTP_400_BAD_REQUEST)
            if 'cancel_reason' not in request_data:
                return Response({ 'message': 'A cancel reason must be provided' }, status=status.HTTP_400_BAD_REQUEST)
            
        # check for blocked status
        if 'status' in request_data and request_data['status'].lower() == 'blocked':
            if 'blocked_reason' not in request_data:
                return Response({ 'message': 'A blocked reason must be provided' }, status=status.HTTP_400_BAD_REQUEST)        

        # check for the fields this type of user can edit (they can edit the status, but not cancel the project)
        if user_access <= 1:
            disallowed_fields = self.partner_only_update_fields()
            messages = {'message': 'You dont have permissions to edit these fields', 'responseObject': []}
            for key in request_data:
                if key in disallowed_fields:
                    messages['responseObject'].append(key)
            return Response(messages, status=status.HTTP_400_BAD_REQUEST)
    
        # if 'estimated_start_date' in request_data or 'estimated_end_date' in request_data:
        #     # check if there's an estimated end or start date in the db ---> We already have it in the db
        #     est_start = project['estimated_start_date']
        #     est_end = project['estimated_start_date']

        #     if 'estimated_start_date' in request_data and est_end is None:
        #         return Response({ 'message': 'An estimated end date must be provided' }, status=status.HTTP_400_BAD_REQUEST)
        #     if 'estimated_end_date' in request_data and est_start is None:
        #         return Response({ 'message': 'An estimated start date must be provided' }, status=status.HTTP_400_BAD_REQUEST)

        return True
    
    def handle_project_status_date_updates(self, request_data, project):
        '''handles updating the dates and the timeline logic'''
        # handle updating project statuses and dates
        if project.status.lower() == 'to-do':
            if 'status' in request_data and request_data['status'].lower() == 'progress':
                request_data['start_date'] =  timezone.now()
        elif project.status.lower() != 'done':
            if 'status' in request_data and request_data['status'].lower() == 'done':
                request_data['end_date'] =  timezone.now()
        
        if 'estimated_start_date' in request_data or 'estimated_end_date' in request_data:
            # we're enforcing the estimated start and end date during creation. Therefore, this will always be there
            est_start = project['estimated_start_date'] if project['estimated_start_date'] != None else request_data['estimated_start_date']
            est_end =project['estimated_end_date'] if project['estimated_end_date'] != None else request_data['estimated_end_date']
            duration = relativedelta(est_end, est_start)
            request_data['estimated_timeline'] = f'{duration.days * 24} hours'

        return request_data