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
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
    verifyEmail
)
urlpatterns = [
    path("create/user/",CreateUserAPIView.as_view(),name="create-user"),
    path('email/verify/', verifyEmail, name="email-verify"), #Frontend should send the token to this endpoint
    path('reset/password/', RequestPasswordResetEmail.as_view(),name="reset-password"),
    path('password/reset/complete/', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('login/', MyTokenObtainPairView.as_view(), name='custom-token'),
    path('refresh/token/', TokenRefreshView.as_view(), name='token-refresh'),
    path("fetch/profile/all/", ProfileListAPIView.as_view(), name="all-profiles"),
    path("fetch/profile/", ProfileDetailAPIView.as_view(), name="profile-details"),
    path("update/profile/", UpdateProfileAPIView.as_view(), name="profile-update"),
    path("fetch/followers/", get_my_followers, name="my-followers"),
    path("<str:username>/following/",FollowUnfollowAPIView.as_view(),name="follow-unfollow"),
]
