from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Task
from django.urls import reverse_lazy


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "todo/list_task.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = Task.objects.filter(status=True)
        return tasks

class CreateTaskView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        '''
        get user id and save before sending
        '''
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateTaskView(LoginRequiredMixin,UpdateView):
    model = Task
    success_url = reverse_lazy('task_list')
    form_class = UpdateTaskFrom
    template_name = "todo/update_task.html"

class DeleteTaskView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

class TaskCompleteView(LoginRequiredMixin,View):
    model = Task