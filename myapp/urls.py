from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('blog/', views.blog),
    path('add-blog/', views.add_blog),
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('signout/', views.signout),
    path('todo_list/', views.TodoListView.as_view(),name='todo_list'),
    path('todo_create/', views.TodoCreateView.as_view(),name='todo_create'),
    path('todo_detail/<int:pk>/', views.TodoDetailView.as_view(), name='todo_detail'),
    path('todo_edit/<int:pk>/edit/', views.TodoEditView.as_view(),name='todo_edit'),
    path('todo_delete/<int:pk>/delete/', views.TodoDeleteView.as_view(),name='todo_delete'),
]
