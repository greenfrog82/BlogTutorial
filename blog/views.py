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
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    logging.debug('request.user.is_authenticated : %s' % request.user.is_authenticated)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('/admin')

    if 'POST' == request.method:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    if isinstance(request.user, AnonymousUser):
        return redirect('/admin')

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # 튜토리얼에는 아래 주석과 같이 처리하라고 되어있지만, request.POST만 전달하여도 정상적으로 동작함.
        # form = PostForm(request.POST, instance=post)
        form = PostForm(request.POST)
        if form.is_valid():
            # 다음 코드를 동작시키면, Post객체가 새로 생성된다.
            # post = form.save(commit=False)
            post = form.save()
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            logging.debug('here?')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
