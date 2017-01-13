from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


# 인증 관련 부분 다음 링크 참고해서 구현하였음.
# http://blog.narenarya.in/right-way-django-authentication.html
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'name': 'username', 'id': 'inputId'}))
    password = forms.CharField(widget=forms.TextInput(
            attrs={
                    'class': 'form-control',
                    'name': 'password',
                    'id': 'inputPassword',
                    'type': 'password'}))


