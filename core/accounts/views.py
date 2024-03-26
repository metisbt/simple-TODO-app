from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from .models import User
from .forms import UserRegisterForm

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    fields = "email","password"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("task_list")


class RegisterPage(FormView):
    model = User
    template_name = "accounts/register.html"
    # fields = ['email', 'password1', 'password2']
    form_class = UserRegisterForm
    success_url = reverse_lazy("task_list")
    redirect_authenticated_user = True


    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("task_list")
        return super(RegisterPage, self).get(*args, **kwargs)
