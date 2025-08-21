from django.urls import path
from tasks.views import LabelListCreateView, LabelDetailView

urlpatterns = [
    path("", LabelListCreateView.as_view(), name="label-list-create"),
    path("<int:pk>/", LabelDetailView.as_view(), name="label-detail"),
]
