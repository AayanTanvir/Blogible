from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json

from .forms import *
from .models import *


class LoginPage(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True
    fields = '__all__'
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse_lazy('home')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            return render(request, 'main/login.html', {
                'form': form,
                'error': "Please enter correct credentials. Note that both fields may be case-sensitive."
            })
    else:
        form = LoginForm()
    
    
    return render(request, 'main/login.html', {'form': form})



def logout_view(request):
    
    logout(request)
    return redirect('login')

def register_page(request):
    context = {}
    form = RegisterForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            pfp = form.cleaned_data['pfp']

            user = authenticate(request, username=username, password=password)
            if pfp:
                Profile.objects.create(user=user, username=username, pfp=pfp)
            else:
                Profile.objects.create(user=user, username=username)

            login(request, user)
            return redirect('home')

    context['form'] = form
    return render(request, 'main/register.html', context)



def landing_page(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, "main/landing_page.html", context)


@login_required()
def home_page(request):
    context = {}
    current_user = request.user
    context['current_user'] = current_user
    
    search_text = request.GET.get('search-text') or ''
    category = request.GET.get('category') or ''
    filter_by = request.GET.get('filter-by') or ''
    
    if (category == '' or category == 'all') and search_text == '' and (filter_by == '' or filter_by == 'none'):
        context['blogs'] = Blog.objects.all()
        
    elif (category != 'all' or category != '') and search_text == '' and (filter_by == '' or filter_by  == 'none'):
        context['blogs'] = Blog.objects.filter(category=category)
        
    elif (category == '' or category == 'all') and search_text == '' and (filter_by != '' or filter_by != 'none'):
        match filter_by:
            case 'most-liked':
                context['blogs'] = Blog.objects.order_by('-likes')
            case 'most-disliked':
                context['blogs'] = Blog.objects.order_by('likes')               
            case 'latest':
                context['blogs'] = Blog.objects.order_by('-date_created')
            case 'oldest':
                context['blogs'] = Blog.objects.order_by('date_created')
            case 'followed-creators-only':
                followed_creators = Profile.get_all_following_creators(current_user)
                context['blogs'] = Blog.objects.filter(user__in=followed_creators)
                
    elif (category == '' or category == 'all') and search_text != '' and (filter_by == '' or filter_by  == 'none'):
        context['blogs'] = Blog.objects.filter(
            Q(title__icontains=search_text) |
            Q(description__icontains=search_text) |
            Q(user__username__iexact=search_text)
        )
    
        
    context['current_category'] = category
    context['search_query'] = search_text
    context['current_filter'] = filter_by

    return render(request, 'main/home.html', context)

@login_required()
def profile_page(request, pk, username):
    context = {}
    user = get_object_or_404(User, id=pk, username=username)
    profile = user.profile
    context['profile'] = profile
    current_user = request.user
    context['current_user'] = current_user

    can_follow = False
    has_followed = Profile.get_follow_status(current_user, profile.id)
    context['has_followed'] = has_followed

    
    if current_user.profile == profile:
        can_follow = False
    else:
        can_follow = True
    context['can_follow'] = can_follow

    follower_count = Profile.get_follower_count(profile.id)
    context['followers'] = follower_count

    blogs = Profile.get_blogs(profile.id)
    context['blogs'] = blogs

    return render(request, 'main/profile_page.html', context)

@login_required()
def edit_profile_page(request, pk, username):
    context = {}
    current_user = get_object_or_404(User, id=pk, username=username)
    context['current_user'] = current_user
    current_profile = current_user.profile
    context['current_profile'] = current_profile
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=current_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_page', pk=pk, username=username)
    else:
        form = ProfileEditForm(instance=current_profile)
        context['form'] = form

    return render(request, 'main/edit_profile.html', context)

@login_required()
def follow_creator_or_unfollow(request, pk, username):
    if request.method == "POST":
        creator = get_object_or_404(Profile, id=pk, username=username)
        follower = request.user.profile

        if creator != follower:
            subscription = Subscribe.objects.filter(creator=creator, follower=follower).first()
        else:
            return HttpResponse('Cannot follow yourself :)')

        if subscription:
            subscription.delete()
            return JsonResponse({'status':'success', 'message':'unfollowed'})
        else:
            Subscribe.objects.create(creator=creator, follower=follower)
            return JsonResponse({'status':'success', 'message':'followed'})

    else:
        return HttpResponse('Bad request 400')

@login_required()
def blog_page(request, pk, title):
    if request.method == 'GET':
        context = {}
        blog = get_object_or_404(Blog, id=pk)
        current_user = request.user
        
        likes_count = Like.objects.filter(blog=blog).count()
        dislikes_count = Dislike.objects.filter(blog=blog).count()
        like_dislike_status = Blog.get_like_dislike_status(blog, current_user.profile)
        
        like_status = like_dislike_status['like_status']
        dislike_status = like_dislike_status['dislike_status']
        
        blog_comments = blog.get_all_comments()
        
        if blog_comments != 'no comments':
            context['comments'] = blog_comments
        else:
            context['comments'] = 'nothing'
        
        context['current_user'] = current_user
        context['blog'] = blog
        context['likes_count'] = likes_count
        context['dislikes_count'] = dislikes_count
        context['like_status'] = like_status
        context['dislike_status'] = dislike_status

        return render(request, 'main/blog_page.html', context)
    
    elif request.method == 'POST':
        comment_text = request.POST.get('form-comment')
        blog = get_object_or_404(Blog, id=pk)
        commenter = request.user.profile
        Comment.objects.create(text=comment_text, blog=blog, commenter=commenter)
        
        return redirect('blog_page', pk=pk, title=title)

        
        

@login_required()
def write_blog(request):
    context = {}
    form = BlogForm()
    current_user = request.user
    context['current_user'] = current_user
    
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            body = form.cleaned_data['body']
            category = form.cleaned_data['category']
            
            Blog.objects.create(title=title, description=description, body=body, category=category, user=request.user)
            return redirect('home')
    
    context['form'] = form
    return render(request, 'main/write_blog.html', context)

@login_required()
def update_blog(request, pk, title):
    current_user = request.user
    blog = get_object_or_404(Blog, id=pk)
    
    if current_user != blog.user:
        return redirect('home')
    else:
        context = {}
        form = BlogForm(instance=blog)
        context['current_user'] = current_user
        context['blog'] = blog
        
        if request.method == "POST":
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                form.save()
                return redirect('blog_page', pk=pk, title=title)
        
        context['form'] = form
        return render(request, 'main/update_blog.html', context)
    
@login_required()
def blog_actions(request, pk, action):
    if request.method == "POST":
        blog = get_object_or_404(Blog, id=pk)
        body = json.loads(request.body)
        
        if action == 'delete':
            blog.delete()
            return JsonResponse({'status':'success'})
        elif action == 'like':
            if body.get('increase'):
                Like.objects.create(user=request.user.profile, blog=blog)
                return JsonResponse({'status':'success'})
            else:
                Like.objects.get(user=request.user.profile, blog=blog).delete()
                return JsonResponse({'status':'success'})
        elif action == 'dislike':
            if body.get('increase'):
                Dislike.objects.create(user=request.user.profile, blog=blog)
                return JsonResponse({'status':'success'})
            else:
                Dislike.objects.get(user=request.user.profile, blog=blog).delete()
                return JsonResponse({'status':'success'})
    else:
        return HttpResponse('Bad request 400')

