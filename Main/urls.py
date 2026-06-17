from django.urls import path
from . import views

urlpatterns = [
    # Landing
    path('', views.landing, name='landing'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # File operations
    path('addFile/', views.addFile, name='addFile'),
    path('editFile/<str:id>/', views.editFile, name='editFile'),
    path('downloadFile/<str:id>/', views.downloadFile, name='downloadFile'),
    path('trashFile/<str:id>/', views.trashFile, name='trashFile'),

    # Trash
    path('trash/', views.trashView, name='trash'),
    path('restoreFile/<str:id>/', views.restoreFile, name='restoreFile'),
    path('permanentDelete/<str:id>/', views.permanentDelete, name='permanentDelete'),

    # Delete (legacy URL kept for backward compat — now redirects to trash)
    path('deleteFile/<str:id>/', views.trashFile, name='deleteFile'),

    # Sharing
    path('shareFile/<str:id>/', views.shareFile, name='shareFile'),
    path('shared/<str:share_id>/', views.sharedFile, name='sharedFile'),

    # Folders
    path('createFolder/', views.createFolder, name='createFolder'),
    path('deleteFolder/<str:id>/', views.deleteFolder, name='deleteFolder'),

    # Profile
    path('profile/', views.profile, name='profile'),
]
