from django.shortcuts import render, redirect
from django.urls import  reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm


from .forms import *

# Create your views here.
class MyLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True
    fields = '__all__'
    authentication_form = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('home')

def logout_view(request):
    logout(request)
    return redirect('login')

class RegisterView(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return redirect('home')
        
        return super(RegisterView, self).form_valid(form)

def landing_page(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, "main/landing_page.html", context)


@login_required()
def home_page(request):
    context = {}
    user = request.user
    context["username"] = user
    
    return render(request, 'main/home.html', context)