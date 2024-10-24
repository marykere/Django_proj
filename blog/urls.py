from django.urls import path
from . import views 
from .views import PostListView, UserPostListView, PostDetailView, CreatePostView, UpdatePostView, DeletePostView

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', CreatePostView.as_view(), name='post-form'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about' )
]
