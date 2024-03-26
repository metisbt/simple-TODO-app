from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='update_task'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
    path('complete/<int:pk>/', TaskCompleteView.as_view(), name='complete_task'),
]