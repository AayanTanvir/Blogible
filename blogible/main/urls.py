from django.urls import path
from .views import *


urlpatterns = [
    path('login/', MyLoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    
    path('', landing_page, name="landing_page"),
    path('home/', home_page, name="home"),
]