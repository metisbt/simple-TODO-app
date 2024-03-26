from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class TaskListView(LoginRequiredMixin,ListView):
    pass

class CreateTaskView(LoginRequiredMixin,CreateView):
    pass

class UpdateTaskView(LoginRequiredMixin,UpdateView):
    pass

class DeleteTaskView(LoginRequiredMixin,DeleteView):
    pass

class TaskCompleteView(LoginRequiredMixin,View):
    pass