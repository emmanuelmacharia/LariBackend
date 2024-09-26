from django.urls import path
from .views import CreateViewInvite, FetchWorkspaceInvites, GetUpdateDeleteViewInvites


urlpatterns = [
    path('', CreateViewInvite.as_view(), name='create_invite_view'),
    path('workspace/<int:id>', FetchWorkspaceInvites.as_view(), name='fetch_workspace_invite'),
    path('action/<str:uuid>', GetUpdateDeleteViewInvites.as_view(), name="action_invite_view"),
]