from rest_framework import serializers
from .models import ProjectPartner
from UserManagement.models import User
from Projects.models import Project


class ProjectPartnerSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectPartner
        fields = '__all__'
        

    def validate(self, data):
        '''validates the project partner information'''
        if not data.get('user'):
            raise serializers.ValidationError("Username field is required")
        if not data.get('project'):
            raise serializers.ValidationError('Project is required')
        if not data.get('user_access_level'):
            raise serializers.ValidationError('User access level is required')
        
        if not User.objects.get(userid=data.get('user')):
            raise serializers.ValidationError("User doesn't exist")
        
        if not Project.objects.get(projectId = data.get('project')):
            raise serializers.ValidationError("Project doesn't exist")
        

    def create(self, validated_data):
        return ProjectPartner.objects.create(**validated_data)
