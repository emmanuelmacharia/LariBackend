from django.urls import path
from .views import CreateViewProject


urlpatterns = [
    path('', CreateViewProject.as_view(), name='create-and-read-all-view')
]