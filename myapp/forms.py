from django import forms
from .models import  Blog,Author
from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

# class SigninForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','password']
#         widgets = {
#             'password': forms.PasswordInput(),  # This hides the password input
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(SigninForm, self).__init__(*args, **kwargs)
#         self.fields['username'].help_text = None
#         self.fields['password'].help_text = None