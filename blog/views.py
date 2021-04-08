from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Blog, Blogger
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from blog.forms import CommentForm
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
    form = CommentForm(request.POST)
    context = {'form':form}
    return render(request, 'blog/add_comment.html', context)

    