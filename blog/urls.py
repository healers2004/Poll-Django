from django.urls import path
from . import views
from blog.feeds import LatestPostsFeed

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tag/<slug:tag_slug>/', views.blog_tag, name='blog_tag'),
    path('rss/', LatestPostsFeed(), name='latest_posts_feed'),
]