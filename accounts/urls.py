from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

#
from .views import send_friend_request, accept_friend_request
#

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path('friends/', views.friends_index, name='friends_index'),
    path('send_request/<int:user_id>/', views.send_friend_request_view, name='send_friend_request'),
    path('accept_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path("user/<int:user_id>/", views.view_user_profile, name="view_user_profile"),
    path("find_friends/", views.find_friends, name="find_friends"),
    path("incoming_requests/", views.incoming_requests, name="incoming_requests"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("profile/<int:user_id>/", views.view_user_profile, name="view_user_profile"),
    path('delete_request/<int:request_id>/', views.delete_friend_request, name='delete_friend_request'),

    # path('delete_friend_request/<int:request_id>/', delete_friend_request, name='delete_friend_request')

    path('friend-request/<int:request_id>/cancel/', views.cancel_friend_request, name='cancel_friend_request'),
    path("profile/<int:user_id>/", views.view_user_profile, name="view_user_profile"),
    path('delete_request/<int:request_id>/', views.delete_friend_request, name='delete_friend_request'),
    path('friend-request/<int:request_id>/cancel/', views.cancel_friend_request, name='cancel_friend_request'),
    path('friend-request/<int:request_id>/delete/', views.delete_friend_request, name='delete_friend_request'),
    path('friends/remove/<int:user_id>/', views.remove_friend, name='remove_friend'),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
]