from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Blog


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'login-username input-field',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'login-pass input-field',
            'placeholder': 'Password',
        })
    
class RegisterForm(UserCreationForm):
    
    pfp = forms.ImageField(
        required=False,
        label="Profile Picture",
        label_suffix="",
        widget=forms.FileInput(attrs= {
            'class': 'register-pfp',
            'placeholder': 'Profile Picture',
            'accept': 'image/*',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required':'',
            'class': 'register-username input-field',
            'placeholder': 'Username',
            'max_length': '20',
            'autocomplete': 'name',
        })
        self.fields["email"].widget.attrs.update({
            'class':'register-email input-field',
            'placeholder': 'Email Address',
            'autocomplete': 'email'
        })
        self.fields["password1"].widget.attrs.update({
            'required': '',
            'class': 'register-pass1 input-field',
            'placeholder': 'Password',
            'min-length':  '8',
        })
        self.fields["password2"].widget.attrs.update({
            'required':  '',
            'class': 'register-pass2 input-field',
            'placeholder': 'Confirm Password',
            'min-length': '8',
        })
        
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'input-field edit-username-input',
            'placeholder': 'Username',
            'max_length': '20',
            'pattern': "^\\S+$",
            'title':'No Spaces Allowed',
        })
        self.fields['bio'].widget.attrs.update({
            'class': 'text-input-field edit-bio-input',
            'placeholder': 'Biography',
        })
        self.fields['pfp'].label = "Profile Picture"
        self.fields['pfp'].label_suffix = ""
        self.fields['pfp'].required = False
        self.fields['pfp'].widget = forms.FileInput(attrs={
            'class': 'edit-pfp',
            'placeholder': 'Profile Picture',
            'accept': 'image/*',
        })

    
    class Meta:
        model = Profile
        fields = ["username", "pfp", "bio"]
        
class BlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs.update({
            'class': 'input-field write-blog-title',
            'placeholder': 'Title',
            'required': 'required',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'text-input-field write-blog-description',
            'placeholder': 'Description',
        })
        self.fields['body'].widget.attrs.update({
            'class': 'text-input-field write-blog-body',
            'placeholder': 'Body',
            'required': 'required',
        })
        self.fields['category'].widget.attrs.update({
            'class': 'write-blog-category',
            'required': 'required',
        })
            
    class Meta:
        model = Blog
        fields = ["title", "description", "body", "category"]
        