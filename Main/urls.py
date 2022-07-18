from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('addFile/', views.addFile, name='addFile'),
    path('downloadFile/<str:id>/', views.downloadFile, name='downloadFile'),
    path('deleteFile/<str:id>/', views.deleteFile, name='deleteFile'),
]
