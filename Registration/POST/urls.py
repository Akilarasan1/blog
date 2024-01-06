from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name = 'home'),
    
     path('posts/', views.index, name='posts'),
    path('posts/<int:id>/edit_post/',views.edit_post, name = 'edit_post'),
    path('posts/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('posts/create/', views.create_post, name='create_post'),
    
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
]