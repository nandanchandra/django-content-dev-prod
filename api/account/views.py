import jwt
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes,renderer_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from djangocontent.settings.local import DOMAIN

from .models import Profile
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer,CreateUserSerializer,MyTokenObtainPairSerializer,ResetPasswordRequestSerializer,SetNewPasswordSerializer

from api.utils.email_utils import Util
from api.utils.pagination import DefaultPagination
from api.utils.renderers import CustomeJSONRenderer
from api.utils.custom_view_exceptions import CantFollowYourself


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
@renderer_classes([CustomeJSONRenderer])
@csrf_exempt
def verifyEmail(request):
    if request.method == 'POST':
        token = request.data.get('token')
        try:
            payload = jwt.decode(token,settings.SIGNING_KEY,algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])
            user.is_email_verified = True
            user.save()
            return Response('User Email Verified', status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            logger.error(str(identifier))
            return Response('Activation Expired', status=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError as identifier:
            logger.error(str(identifier))
            return Response('Invalid token', status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(str(e))
            return Response('Technical Issuse')

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    renderer_classes = [CustomeJSONRenderer]

    def post(self, request):    
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user=User.objects.get(email=request.data['email'])
                uidb64=urlsafe_base64_encode(force_bytes(user.id))
                absurl = f"{DOMAIN}/password/reset/complete/?uidb={str(uidb64)}"
                email_body = 'Hello '+user.first_name+',<br><br>Lost your password? No worries! Just '+ f"<button type=\"button\"><a href={absurl} style=\" text-decoration : none; color: black; \">Click here</a></button>" +' to set a new password and keep your account secure.<br> Alternatively, you can click the link below to reset:<br>'+f"{absurl}" +'<br><br>If you are still facing some trouble in logging into your account, or if you did not request to update/reset your password, please inform us immediately by sending an email to chandranandan.chandrakar@gmail.com or submitting a support request <a href="chandranandan16@gmail.com">here</a>.<br>'+'<br><br>Team,<br>DjangoContent<br>'+'______________________________________________________________________________________________<br>'+'This is an automatically generated email, please do not reply. If you need to contact us, please send us an email at<br>'+'chandranandan.chandrakar@gmail.com<br>'+'<br>Copyright © 2022 DjangoContent<br>'+'<br>All rights reserved.'
                data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Reset your password for DjangoContent'}
                Util.send_email(data)  
                return Response('Link Send To Email',status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(str(e))
                return Response('User Does Not Exits',status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    renderer_classes = [CustomeJSONRenderer]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response('Password reset success', status=status.HTTP_200_OK)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    queryset = ''

class ProfileListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    renderer_classes = (CustomeJSONRenderer,)
    pagination_class = DefaultPagination

class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (CustomeJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        try:
            profile = self.queryset.get(user__id=request.user.id)
        except Profile.DoesNotExist:
            raise NotFound("A profile with the credentails does not exist")
        serializer = self.serializer_class(profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [CustomeJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request):
        try:
            self.queryset.get(user__id=request.user.id)
        except Profile.DoesNotExist:
            raise NotFound("A profile does not exist")
        data = request.data
        serializer = UpdateProfileSerializer(instance=request.user.profile, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@renderer_classes([CustomeJSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def get_my_followers(request):
    try:
        specific_user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        raise NotFound("User with that username does not exist")

    userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
    user_followers = userprofile_instance.followed_by.all()
    serializer = FollowingSerializer(user_followers, many=True)
    return Response({"followers": serializer.data,"followers_count": len(serializer.data)}, status=status.HTTP_200_OK)


class FollowUnfollowAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer
    renderer_classes = [CustomeJSONRenderer]

    def get(self, request,username):
        try:
            specific_user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        my_following_list = userprofile_instance.following_list()
        serializer = ProfileSerializer(my_following_list, many=True)
        return Response({"following": serializer.data,"following_count": len(serializer.data)}, status=status.HTTP_200_OK)

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
            return Response(f"You already follow {specific_user.username}", status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.follow(userprofile_instance)
        subject = "A new user follows you"
        message = f"Hi there {specific_user.username}!!, the user {current_user_profile.user.username} now follows you"
        recipient_list = [specific_user.email]
        Util.send_email(data={'email_subject':subject, 'email_body':message,"to_email":recipient_list})
        return Response(f"You now follow {specific_user.username}", status=status.HTTP_200_OK)

    def delete(self, request, username):
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")
        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile
        if not current_user_profile.check_following(userprofile_instance):
            return Response(f"You do not follow {specific_user.username}", status=status.HTTP_400_BAD_REQUEST)
        current_user_profile.unfollow(userprofile_instance)
        return Response(f"You have unfollowed {specific_user.username}", status=status.HTTP_200_OK)