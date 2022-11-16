import jwt
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from djangocontent.settings.local import DEFAULT_FROM_EMAIL,DOMAIN

from .models import Profile
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer,CreateUserSerializer,MyTokenObtainPairSerializer

from api.utils.email_utils import Util
from api.utils.pagination import ProfilePagination
from api.utils.renderers import CustomeJSONRenderer
from api.utils.custom_view_exceptions import CantFollowYourself, NotYourProfile


User = get_user_model()
logger = logging.getLogger(__name__)
# Create your views here.
class CreateUserAPIView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    renderer_classes = (CustomeJSONRenderer,)

    def post(self, request):
        serializer=CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            try:
                user = User.objects.get(email=request.data['email'])
                token = RefreshToken.for_user(user).access_token
                absurl = f"{DOMAIN}/email/verify/?token={str(token)}"
                email_body = 'Hello '+user.first_name +'<br><br>Thank you for signing up on DjangoContent. To get started, please ' + f"<button type=\"button\"><a href={absurl} style=\" text-decoration : none; color: black; \">Click here</a></button>" + ' to verify your email.<br> Alternatively, you can click the link below to verify:<br><br>'+f"{absurl}" + '<br><br> If you didn’t ask to verify this email, please let us know.' + '<br><br>Team,<br>DjangoContent<br>'+'______________________________________________________________________________________________<br>'+'This is an automatically generated email, please do not reply. If you need to contact us, please send us an email at<br>'+'chandranandan.chandrakar@gmail.com<br>'+'<br>Copyright © 2021 implicitdefcncdragneel<br>'+'<br>All rights reserved.'
                data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Please verify your email to join DjangoContent'}
                Util.send_email(data)
            except Exception as e:
                logger.error(str(e))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def verifyEmail(request):
    if request.method == 'POST':
        token = request.data.get('token')
        try:
            payload = jwt.decode(token,settings.SIGNING_KEY,algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])
            user.is_email_verified = True
            user.save()
            return Response({'message': 'User Email Verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            logger.error(str(identifier))
            return Response({'error': 'Activation Expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError as identifier:
            logger.error(str(identifier))
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(str(e))
            return Response({'error':'Technical Issuse'})

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    queryset = ''

class ProfileListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    renderer_classes = (CustomeJSONRenderer,)
    pagination_class = ProfilePagination

class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (CustomeJSONRenderer,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [CustomeJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile
        
        data = request.data
        serializer = UpdateProfileSerializer(instance=request.user.profile, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_my_followers(request, username):
    try:
        specific_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound("User with that username does not exist")

    userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)

    user_followers = userprofile_instance.followed_by.all()
    serializer = FollowingSerializer(user_followers, many=True)
    
    formatted_response = {
        "status_code": status.HTTP_200_OK,
        "followers": serializer.data,
        "num_of_followers": len(serializer.data),
    }
    return Response(formatted_response, status=status.HTTP_200_OK)


class FollowUnfollowAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    def get(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        my_following_list = userprofile_instance.following_list()
        serializer = ProfileSerializer(my_following_list, many=True)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "users_i_follow": serializer.data,
            "num_users_i_follow": len(serializer.data),
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

    def post(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        if specific_user.pkid == request.user.pkid:
            raise CantFollowYourself

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You already follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.follow(userprofile_instance)

        subject = "A new user follows you"
        message = f"Hi there {specific_user.username}!!, the user {current_user_profile.user.username} now follows you"
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [specific_user.email]
        Util.send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        
        formatted_response = {
                "status_code": status.HTTP_200_OK,
                "detail": f"You now follow {specific_user.username}",
            }
        return Response(formatted_response, status=status.HTTP_200_OK)

    def delete(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if not current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You do not follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.unfollow(userprofile_instance)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "detail": f"You have unfollowed {specific_user.username}",
        }
        return Response(formatted_response, status=status.HTTP_200_OK)