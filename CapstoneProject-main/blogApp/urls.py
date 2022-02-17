from typing import ValuesView
from django.urls import path
from .import views

app_name='blogApp'

urlpatterns = [

    path('', views.BlogListView.as_view(), name='blog_list'),
    path('<slug:slug>/', views.TopicListView.as_view(), name='topic_list'),
    path('<str:blog>/<slug:slug>/', views.PostListView.as_view(), name='post_list'),
    path('<str:blog>/<str:slug>/create/', views.PostCreateView.as_view(),name='post_create'),
    path('<str:blog>/<str:topic>/<slug:slug>/', views.PostDetailView.as_view(),name='post_detail'),
    path('<str:blog>/<str:topic>/<slug:slug>/update/', views.PostUpdateView.as_view(),name='post_update'),
    path('<str:blog>/<str:topic>/<slug:slug>/delete/', views.PostDeleteView.as_view(),name='post_delete'),


   
]