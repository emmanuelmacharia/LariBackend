from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ProjectUpdateSerializer, ProjectsSerializers
from core.helpers.auth_token_decorator import auth_token_validator
from ProjectPartnerManagement.models import ProjectPartner
from .models import Project

class CreateViewProject(APIView):
    '''create and read all api view'''
    serializer_class = ProjectsSerializers

    @auth_token_validator
    def post(self, request, format=None):
        '''creates a new project'''

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        error_message = "Sorry, we cant complete this request at the moment, please try again"
        error_response = Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save()
        except:
            return error_response

        try:
            project = Project.objects.get(projectId= serializer.data['projectId'])
            ProjectPartner.objects.create(user=request.user, project=project, user_access_level='3')
        except:
           return error_response
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        user = self.request.user
        # Get projects where the user is a partner
        user_projects = ProjectPartner.objects.filter(user=user).values('project_id')
        project_ids = [item['project_id'] for item in user_projects]
        return Project.objects.filter(pk__in=project_ids)

    @auth_token_validator
    def get(self, request, *args, **kwargs):
        '''gets all projects. Should only get projects relative to you; rather than all the projects'''
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)
    

class GetUpdateDeleteViewProject(APIView):
    '''can fetch single project; update and delete projects'''

    serializer_class = ProjectUpdateSerializer

    def get_queryset(self,project_id):
        user = self.request.user
        print(user)
        # Get projects where the user is a partner
        try:
            user_project = ProjectPartner.objects.get(user=user, project_id=project_id)
            return (user_project.project, user_project.user_access_level, )
        except:
            return ()

    @auth_token_validator
    def get(self, request, id):
        ''''gets a single project based on ID - fetches all project details'''
        queryset  = self.get_queryset(id)
        if not len(queryset):
            return Response({'message': 'Project not found or you don\'t have access to it'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset[0])
        access = queryset[1]
        response = self.serializer_class().create_detailed_response(serializer.data, access)
        return Response(response, status=status.HTTP_200_OK)


    @auth_token_validator
    def put(self, request, id):
        '''updates project details (aside from project partners - this will be done with another api)'''
        print(request.data)
        queryset = self.get_queryset(id)
        if not len(queryset):
            return Response({'message': 'Project not found or you don\'t have access to it'}, status=status.HTTP_404_NOT_FOUND)
        project = queryset[0]
        request_data = request.data
        validated_status = self.serializer_class().validate_status_permutations(request.data, project, queryset[1])

        if validated_status == True:
            request_data = self.serializer_class().handle_project_status_date_updates(request.data, project)
        else:
            return validated_status
        
        # handle update records
        serializer = self.serializer_class(project, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = self.serializer_class().create_detailed_response(serializer.data, queryset[1])
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    @auth_token_validator
    def  delete(self, request, id):
        '''deletes a project'''
        pass
    