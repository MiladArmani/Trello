from django.urls import path
from .views import WorkspaceListCreateView, WorkspaceDetailView, WorkspaceInviteView
from boards.views import BoardListCreateView


urlpatterns = [
    path("", WorkspaceListCreateView.as_view(), name="workspace-list-create"),
    path("<int:pk>/", WorkspaceDetailView.as_view(), name="workspace-detail"),
    path("<int:pk>/invite/", WorkspaceInviteView.as_view(), name="workspace-invite"),
    path('<int:workspace_pk>/boards/', BoardListCreateView.as_view(), name='workspace-boards'),
]
