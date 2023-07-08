from rest_framework import serializers
from .models import Project

class ProjectsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['projectId']
        
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
    

