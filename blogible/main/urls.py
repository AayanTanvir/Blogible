from django.urls import path
from .views import *


urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_page, name="register"),

    path('', landing_page, name="landing_page"),
    path('home/', home_page, name="home"),
    path('profile/<str:pk>/<str:username>/', profile_page, name="profile_page"),
    path('profile/edit/<str:pk>/<str:username>/', edit_profile_page, name="edit-profile"),
    path('blogs/<str:pk>/<str:title>/', blog_page, name="blog_page"),
    path('blogs/write/', write_blog, name="write_blog"),
    path('blogs/update/<str:pk>/<str:title>/', update_blog, name="update_blog"),
    
    path('blog/<str:action>/<str:pk>/', blog_actions, name="blog_actions"),
    path('profile/follow/<str:pk>/<str:username>/', follow_creator_or_unfollow, name="follow-creator"),
]