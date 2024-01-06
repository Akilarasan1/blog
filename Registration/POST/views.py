from django.shortcuts import render, redirect,get_object_or_404

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import  login_required

##############

def index(request):
    posts = Post.objects.all()
    context = { 'posts':posts }
    return render(request, 'users/index.html',context)


@login_required
def delete_post(request, id):
    queryset = Post.objects.filter(author = request.user)
    post = get_object_or_404(queryset, pk = id)
    context = {'post':post}
    
    
    if request.method == 'GET':
        return render(request, 'users/Post_confirm_delete.html', context)
    
    elif request.method == 'POST':
        post.delete()
        messages.success(request, 'the post has been deleted success')
        
        return redirect('posts')


@login_required    
def edit_post(request, id):
    queryset = Post.objects.filter(author = request.user)
    
    post = get_object_or_404(queryset, pk = id)
    
    if request.method == 'GET':
        context = {'from': PostForm(instance = post), 'id':id}
        return render(request, 'users/post_form.html')
    
    
    elif request.method == "POST":
        form = PostForm(request.Post, instance = post)
        if form.is_valid():
            form.save()
            messages.success(request, 'the post has been updated successfully')
            return redirect('posts')
        else:
            messages.error(request, 'please correct the following eror')
            return render(request, 'blog/post_form.html', {'form': form})
        
        
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if request.method == 'GET':
        context = {'form': PostForm()}
        return render(request, 'users/post_form.html', context)

    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Create post instance but don't save to the database yet
            post.author = request.user  # Set the author to the current user
            post.save()  # Now save the post to the database

            messages.success(request, 'The post has been created successfully')
            return redirect('posts')

        else:
            messages.error(request, 'Please correct the following error')
            return render(request, 'users/post_form.html', {'form': form})



########################## sign in and sign up #################


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('posts')
        else:
            return render(request, 'users/register.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', {'form':form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('posts')
            
        messages.error(request, f'Invalid username or password') 
        return render(request, 'users/login.html', {'form':form})


def sign_out(request):
    logout(request)
    messages.success(request, f'you have been logged out.')
    return redirect('login')   