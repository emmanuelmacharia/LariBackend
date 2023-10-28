from django.urls import path
from .views import CreateViewProject, GetUpdateDeleteViewProject


urlpatterns = [
    path('', CreateViewProject.as_view(), name='create-and-read-all-view'),
    path('<int:id>', GetUpdateDeleteViewProject.as_view(), name="fetch-and-update-project-details-view")
]