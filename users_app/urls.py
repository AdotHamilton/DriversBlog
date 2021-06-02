from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('profile', views.displayMyProfile),
    path('submitpfp', views.updateProfile),
    path('meets', views.meets),
    path('discussions', views.discussionsHome),
    path('discussions/<int:id>', views.discussionPage),
    path('post', views.makePost),
    path('deletePost/<int:id>', views.deletePost),
    path("likePost", views.likePost),
    path("users/<int:id>", views.displayUser),
    path("users/<int:id>/followuser", views.followUser)

]