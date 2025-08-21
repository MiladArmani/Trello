from django.urls import path, include
from .views import BoardListCreateView, BoardDetailView
from tasks.views import BoardReportView

urlpatterns = [
    # boards under a workspace
    path("<int:workspace_pk>/", BoardListCreateView.as_view(), name="board-list-create"),
    path("<int:workspace_pk>/<int:pk>/", BoardDetailView.as_view(), name="board-detail"),

    # nested resources
    path("<int:workspace_pk>/<int:board_pk>/tasks/", include("tasks.urls")),
    path("<int:workspace_pk>/<int:board_pk>/labels/", include("labels.urls")),
    path("<int:workspace_pk>/<int:board_pk>/reports/", BoardReportView.as_view(), name="board-report"),
]
