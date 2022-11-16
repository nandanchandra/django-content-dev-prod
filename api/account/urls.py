from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    FollowUnfollowAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    UpdateProfileAPIView,
    get_my_followers,
    MyTokenObtainPairView,
    CreateUserAPIView,
    verifyEmail
)
urlpatterns = [
    path("create/user/",CreateUserAPIView.as_view(),name="create-user"),
    path('email/verify/', verifyEmail, name="email-verify"), #Frontend should send the token to this endpoint
    path('login/', MyTokenObtainPairView.as_view(), name='custom-token'),
    path('refresh/token/', TokenRefreshView.as_view(), name='token-refresh'),
    path("fetch/all/profile/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("user/<str:username>/", ProfileDetailAPIView.as_view(), name="profile-details"),
    path("update/<str:username>/", UpdateProfileAPIView.as_view(), name="profile-update"),
    path("<str:username>/followers/", get_my_followers, name="my-followers"),
    path("<str:username>/follow/",FollowUnfollowAPIView.as_view(),name="follow-unfollow"),
]
