from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("update-profile/", views.updateProfile, name="update-profile"),
    path("change-password/", views.changePassword, name="password-change"),
    path("", views.home, name="home"),
    path("room/<int:pk>/", views.room, name="room"),
    path("topics/", views.topicsPage, name="topics"),
    path("activity/", views.activityPage, name="activity"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<int:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<int:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<int:pk>/", views.deleteMessage, name="delete-message"),
]
