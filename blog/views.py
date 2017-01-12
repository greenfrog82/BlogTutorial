from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from .models import Post
from .forms import PostForm
import logging


logging.basicConfig(format='[%(levelname)s][%(funcName)s] %(message)s', level=logging.DEBUG)
logging.debug('initialize view.py')

def post_list(request):
    logging.debug('call post_list')
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def test_post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/test_post_list.html', {'posts': posts})

def post_detail(request, pk):
    logging.debug('call post_detail')
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    logging.debug('user : %s' % request.user)
    logging.debug('method : %s' % request.method)
    logging.debug('body : %s' % request.body)

    if isinstance(request.user, AnonymousUser):
        return redirect('/admin')

    if 'POST' == request.method:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            logging.debug('author : %s' % post.author)
            post.publish()
            return redirect('post_detail', pk=post.pk)
        else:
            logging.debug('The form value is not valied.')
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    logging.debug('call post_edit')

    if isinstance(request.user, AnonymousUser):
        return redirect('/admin')

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # 튜토리얼에는 아래 주석과 같이 처리하라고 되어있지만, request.POST만 전달하여도 정상적으로 동작함.
        # form = PostForm(request.POST, instance=post)
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})
