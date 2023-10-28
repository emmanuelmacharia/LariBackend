from functools import wraps
from rest_framework.request import Request
from rest_framework.response import Response
from ProjectPartnerManagement.models import ProjectPartner

def validate_project_access(f):
    '''
    decorator that validates someone's access and access level to a project;
    Should return project access levels or None depending on the user
    '''
    @wraps(f)
    def wrapper(*args, **kwargs):
        "Checks the project partners table and validates the user's access level"
        user = ''
        for arg in args:
            if not isinstance(arg, Request):
                continue
            user = arg.user
            break

        try:
            '''fetch the role of the partner for the particular project'''
        except:
            ''''if '''

