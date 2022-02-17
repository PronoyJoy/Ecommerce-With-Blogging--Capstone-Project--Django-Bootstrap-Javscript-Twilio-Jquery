from django.urls import path
from .import views

app_name='noteSellingApp'

urlpatterns = [

    path('', views.StandardListView.as_view(), name='standard_list'),
    path('search/',views.searchbar,name='searchbar'),
    path('download/',views.codetrick,name='download'),
    path('autosuggest/',views.autosuggest,name='autosuggest'),
    path('<slug:slug>/', views.CourseListView.as_view(), name='course_list'),
    path('<str:standard>/<slug:slug>/', views.LessonListView.as_view(), name='lesson_list'),
    path('<str:standard>/<str:slug>/create/', views.LessonCreateView.as_view(),name='lesson_create'),
    path('<str:standard>/<str:course>/<slug:slug>/', views.LessonDetailView.as_view(),name='lesson_detail'),
    path('<str:standard>/<str:course>/<slug:slug>/update/', views.LessonUpdateView.as_view(),name='lesson_update'),
    path('<str:standard>/<str:course>/<slug:slug>/delete/', views.LessonDeleteView.as_view(),name='lesson_delete'),


   
]