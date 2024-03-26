from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Task
from django.urls import reverse_lazy
from .forms import UpdateTaskFrom


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = "todo/list_task.html"
    context_object_name = "tasks"

    def get_queryset(self):
        tasks = Task.objects.all()
        return tasks

class CreateTaskView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title"]
    success_url = '/todo/list_task.html'

    def form_valid(self, form):
        '''
        get user id and save before sending
        '''
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateTaskView(LoginRequiredMixin,UpdateView):
    model = Task
    success_url = '/todo/list_task.html'
    form_class = UpdateTaskFrom
    template_name = "todo/update_task.html"

class DeleteTaskView(LoginRequiredMixin,DeleteView):
    model = Task
    success_url = '/todo/list_task.html'

class TaskCompleteView(LoginRequiredMixin,View):
    model = Task
    success_url = '/todo/list_task.html'

    def get(self, request, *args, **kwargs):
        object = Task.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)