from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from ckeditor.fields import RichTextField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=25, default="", blank=False, unique=True)
    bio = models.TextField(blank=True, null=True)
    pfp = models.ImageField(
        upload_to="pfp/",
        default="pfp/pfp.png",
        height_field="img_height",
        width_field="img_width",
        max_length=255,
        null=True
    )
    img_width = models.PositiveIntegerField(blank=True, null=True)
    img_height = models.PositiveIntegerField(blank=True, null=True)

    # Get the blogs posted by the profile
    def get_blogs(pk):
        profile = Profile.objects.get(id=pk)
        user = profile.user

        if user:
            return Blog.objects.filter(user=user)
        return None
    
    def get_follower_count(pk):
        creator = Profile.objects.get(id=pk)
        count = Subscribe.objects.filter(creator=creator).count()
        return count
        
    def get_follow_status(follower_user, creator_profile_id):
        try:
            follower_profile = Profile.objects.get(user=follower_user)
            creator = Profile.objects.get(id=creator_profile_id)
            Subscribe.objects.get(follower=follower_profile, creator=creator)
            return True
        except Subscribe.DoesNotExist:
            return False
        except Profile.DoesNotExist:
            return False
        
    def get_all_following_creators(user):
        subscriptions = Subscribe.objects.filter(follower=user.profile)
        following_creators = subscriptions.values_list('creator', flat=True)
        creator_users = User.objects.filter(id__in=following_creators)
        return creator_users

    def __str__(self):
        return self.username
    
class Subscribe(models.Model):
    
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.username} followed {self.creator.username}"

class Blog(models.Model):
    BLOG_CATEGORIES = [
        ("general", "General"),
        ("sports", "Sports"),
        ("food", "Food"),
        ("gaming", "Gaming"),
        ("politics", "Politics"),
        ("fitness", "Fitness"),
        ("medical", "Medical"),
        ("nature", "Nature"),
        ("technology", "Technology"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(User, related_name='blog', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=60, null=True, blank=False, unique=True)
    body = RichTextField(blank=False, default="")
    description = models.TextField(max_length=160, default="", blank=False, unique=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    category = models.CharField(max_length=255, default="None", choices=BLOG_CATEGORIES)
    
    def get_like_dislike_status(blog, user_profile):
        status = {}
        has_liked = Like.objects.filter(blog=blog, user=user_profile) or ''
        has_disliked = Dislike.objects.filter(blog=blog, user=user_profile) or ''
        
        if has_liked == '' and has_disliked != '':
            status['like_status'] = 'not_liked'
            status['dislike_status'] = 'disliked'
            return status
        elif has_liked != '' and has_disliked == '':
            status['like_status'] = 'liked'
            status['dislike_status'] = 'not_disliked'
            return status
        elif has_liked == '' and has_disliked == '':
            status['like_status'] = 'not_liked'
            status['dislike_status'] = 'not_disliked'
            return status
        
    def get_all_comments(self):
        comments = Comment.objects.filter(blog=self)
        if comments.exists():
            return comments
        else:
            return 'no comments'
        
    def __str__(self):
        return self.title
    


class Comment(models.Model):
    text = models.TextField(blank=False, default="")
    blog  = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"{self.commenter.username} commented on {self.blog.title}"
    
class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog', 'user'], name='unique_like_per_user_blog')
        ]
    
    def __str__(self):
        return f'{self.user.username} liked {self.blog.title}'

class Dislike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog', 'user'], name='unique_dislike_per_user_blog')
        ]
    
    def __str__(self):
        return f'{self.user.username} disliked {self.blog.title}'