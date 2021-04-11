from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from blog.models import Blog, Blogger
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from blog.forms import CommentForm, BlogForm
from django.utils import timezone
import datetime

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