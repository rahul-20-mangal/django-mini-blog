from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('add_comment/<int:pk>/',views.add_comment, name='add-comment'),
    path('edit_comment/<int:pk>/',views.edit_comment, name='edit-comment'),
    path('delete_comment/<int:pk>/',views.delete_comment, name='delete-comment'),
    path('create-blog/', views.create_blog, name='create-blog'),
    path('edit-blog/<int:pk>/', views.edit_blog, name='edit-blog'),
    path('delete-blog/<int:pk>/', views.delete_blog, name='delete-blog'),
]