from django.shortcuts import redirect, render
from django.views import generic
from django.contrib.auth import login
from .models import User
from .forms import RegisterForm


class UserRegister(generic.CreateView):
    model = User
    form_class = RegisterForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('/')
        return render(request, 'accounts/user_form.html', context)


class UserLogoutConfirm(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/logout_confirm.html')
