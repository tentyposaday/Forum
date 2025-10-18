from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, user_logged_in, logout
from django.contrib.auth.decorators import login_required
from . import forms, models

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request ,user)
            return redirect('theforum:homepage')
    else:
        form = UserCreationForm()

    return render(request, 'html/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('theforum:homepage')
    if request.method == 'POST':
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next') or 'theforum:homepage'
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'html/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('theforum:login')

@login_required(login_url='/form/login/')
def homepage(request):
    if request.method == 'POST':
        form = forms.CreateThread(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            thread = models.Thread(name=name)
            thread.save()
            return redirect('theforum:thread', slug=thread.slug)

    else:
        form = forms.CreateThread()
        
    threads = models.Thread.objects.all()
    return render(request, 'html/index.html', {'username': request.user.username, 'threads' : threads, 'form': form})

def thread_view(request, slug):
    thread = get_object_or_404(models.Thread, slug=slug)

    if request.method == 'POST':
        form = forms.CreatePost(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            post = models.Post(title=title, text=text, user=request.user, thread=thread)
            post.save()
            return redirect('theforum:thread', slug=thread.slug)

    else:
        form = forms.CreatePost()

    posts = thread.posts.all()
    return render(request, 'html/thread.html', { 'posts' : posts , 'thread' : thread, 'username': request.user.username, 'form': form })

def post_view(request, slug):
    post = get_object_or_404(models.Post, slug=slug)
    if request.method == 'POST':
        form = forms.CreateComment(request.POST)
        post = get_object_or_404(models.Post, slug=slug)
        if form.is_valid():
            text = form.cleaned_data["text"]
            comment = models.Comment(text=text, user=request.user, post=post)
            comment.save()
            return redirect('theforum:post', slug=post.slug)

    else:
        form = forms.CreateComment()
    
    comments = post.comments.all()
    threadslug = post.thread.slug
    return render(request, 'html/post.html', {'post': post, 'comments': comments, 'username': request.user.username, 'form': form, 'thread': threadslug })