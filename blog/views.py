from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Blog, Blogger
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
