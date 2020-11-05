from django.urls import path
from .views import (
	PostListView, 
	PostDetailView, 
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
        UserPostListView,
        AnnouncementListView,
	AnnouncementCreateView,
)
from . import views

urlpatterns = [
    #path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), # primary key
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/new/admin', AnnouncementCreateView.as_view(), name='announcement-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('announcements/', AnnouncementListView.as_view(), name='announcements')
]
