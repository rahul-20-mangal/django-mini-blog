from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from blog.models import Blog, Blogger, Comment
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from blog.forms import CommentForm, BlogForm
from django.utils import timezone
import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    
    num_blog = Blog.objects.all().count()

    num_blogger = Blogger.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_blog': num_blog,
        'num_blogger': num_blogger,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5

    def get_queryset(self):
        return Blog.objects.order_by('-post_date')

class BlogDetailView(generic.DetailView):
    model = Blog

class BloggerListView(generic.ListView):
    model = Blogger

class BloggerDetailView(generic.DetailView):
    model = Blogger



@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = get_object_or_404(Blog, pk = pk)
            comment.date_time = timezone.now()
            comment.user = request.user
            comment.save()
            
            return redirect('blog-detail', pk=pk)
    
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment.html', {'form': form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.save()
            
        return redirect('blog-detail', pk=comment.blog.pk)
    
    context = {
        "form":form
    }
    return render(request, 'blog/edit_comment.html', context)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog_id = comment.blog.pk
    comment.delete()

    return redirect('blog-detail', pk=blog_id)

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)
            if Blogger.objects.filter(name=request.user).exists():
                blog.blog_author = Blogger.objects.get(name=request.user)
            else:   
                blog.blog_author = Blogger.objects.create(name=request.user)
            blog.post_date = datetime.date.today()
            blog.save()
            return redirect('blogs')
    
    else:
        form = BlogForm()

    return render(request, 'blog/create_blog.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})