from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('blog/', views.PostView.as_view(), name='posts'),
    path('blog/<slug:slug>', views.PostDetailView.as_view(), name='post'),
    path('postBlog/', views.PostBlog.as_view(), name='postBlog'),
    path('blog/<slug:slug>/edit/', views.EditPostView.as_view(), name='edit_post'),
    path('blog/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('page/<int:page_number>/', views.IndexView.as_view(), name='index_paginated'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('postlist/', views.PostList.as_view(template_name="post_list.html"), name='post-list'),
    path('admin/', admin.site.urls),
]