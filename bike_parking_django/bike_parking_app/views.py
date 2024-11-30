# from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from bike_parking_app.models import CustomUser, BikeRackData,Achievements,Badge,NewMarker,DeleteMarker
from rest_framework.generics import GenericAPIView, RetrieveAPIView,RetrieveUpdateAPIView,CreateAPIView,ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import login, logout
from rest_framework.views import APIView, Response
from rest_framework import permissions, status, generics
from rest_framework.authentication import SessionAuthentication
from .validations import custom_validation,validate_username,validate_password
from .serializers import UserRegisterSerializer, UserLoginSerializer,UserSerializer,BikeRackDataSerializer,AchievementsSerializer,BadgeSerializer,LeaderboardSerializer,PasswordResetRequestSerializer,SetNewPasswordSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import get_object_or_404
from bike_parking_app.utils import send_verification_email
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes,force_str
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from .serializers import NewMarkerSerializer

UserModel = get_user_model()

# Create your views here.
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,) 
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                send_verification_email(request, user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(UserModel, pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)

class resend_verification_email(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(email=email)
            if user.is_email_verified:
                return Response({'message': 'Email is already verified'}, status=status.HTTP_400_BAD_REQUEST)

            # Invalidate previous token by generating a new token
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            frontend_url = "https://dot-bikerack-frontend.onrender.com/login"
            verification_link = f"{frontend_url}?uid={uid}&token={token}"

            send_mail(
                'Verify your email address',
                f'Please verify your email address by clicking the following link: {verification_link}',
                'adiel_rodriguez21@outlook.com',
                [user.email],
                fail_silently=False,
            )

            return Response({'message': 'Verification email resent successfully'}, status=status.HTTP_200_OK)

        except UserModel.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetRequest(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = UserModel.objects.filter(email=email).first()
            if user:
                token = account_activation_token.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                frontend_url = "https://dot-bikerack-frontend.onrender.com"
                mail_subject = 'Reset your password'
                print('useremail',user.email)
                message = f"""
                Hi {user.username},

                You requested a password reset. Click the link below to reset your password:

                {frontend_url}/reset-password?uid={uid}&token={token}

                If you did not request this, please ignore this email.

                Thanks,
                Your Team
                """
                send_mail(
                    mail_subject,
                    message,
                    'adiel_rodriguez21@outlook.com',
                    [user.email],
                    fail_silently=False,
                )
            return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPassword(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = UserModel.objects.get(pk=uid)
                if account_activation_token.check_token(user, token):
                    user.set_password(serializer.validated_data['password'])
                    user.save()
                    return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
                return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotCredentialsRequest(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(email=email)
            
            # Create the message with the user's credentials
            mail_subject = 'Your Account Credentials'
            message = f"""
            Hi {user.username},

            Here are your account credentials:

            Username: {user.username}
            Email: {user.email}
            Phone Number: {user.phone_number}

            Please keep this information safe.

            Thanks,
            Your Team
            """
            send_mail(
                mail_subject,
                message,
                'adiel_rodriguez21@outlook.com',
                [user.email],
                fail_silently=False,
            )

            return Response({'message': 'Your account credentials have been sent to your email.'}, status=status.HTTP_200_OK)

        except UserModel.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        assert validate_username(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user   

class BikeRackDataDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = BikeRackData.objects.all()
    serializer_class = BikeRackDataSerializer
    lookup_field = 'Site_ID'

class BikeRackDataCreate(generics.CreateAPIView):
    queryset = BikeRackData.objects.all()
    serializer_class = BikeRackDataSerializer

class BikeRackDataView(APIView):
    def get(self, request):
        # Retrieve all bike rack data
        bike_racks = BikeRackData.objects.all()
        serializer = BikeRackDataSerializer(bike_racks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = BikeRackDataSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                site_ID = request.data.get('site_ID')

                if site_ID:
                    username = request.data.get('user')

                    try:
                        user = CustomUser.objects.get(username=username)

                        if user.assessment_ids:
                            assessment_ids = user.assessment_ids.split(",")
                            if site_ID not in assessment_ids:
                                assessment_ids.append(site_ID)
                        else:
                            assessment_ids = [site_ID]

                        user.assessment_ids = ",".join(assessment_ids)
                        user.assessment_count = len(assessment_ids)
                        user.save()

                        # Assign achievements and emblems based on thresholds
                        self.assign_achievement(user)
                        self.assign_emblem(user)  # Call assign_emblem after assigning achievements

                        return Response({'message': 'Bike rack data, achievements, and badges saved successfully!'}, status=status.HTTP_201_CREATED)

                    except CustomUser.DoesNotExist:
                        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                else:
                    return Response({'error': 'site_ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def assign_achievement(self, user):
        # Define the achievement thresholds
        achievement_thresholds = [
            (2, "Trailblazer"),
            (10, "Map Master"),
            (20, "Surveyor"),
            (50, "Community Builder")
        ]

        for threshold, name in achievement_thresholds:
            if user.assessment_count >= threshold:
                achievement, created = Achievements.objects.get_or_create(name=name)
                if achievement not in user.achievements.all():
                    user.achievements.add(achievement)
                    user.achievements_completed += 1  # Increment achievements_completed
                    user.save()  # Save the updated count

    def assign_emblem(self, user):
        emblem_thresholds = [
            (1, "Infrastructure Advocate"),    
            (3, "Urban Explorer"),
            (5, "Assessment Champion"),
            (10, "Geofence Guru")
        ]

        # Count the user's current achievements
        achievement_count = user.achievements.count()

        for threshold, name in emblem_thresholds:
            if achievement_count >= threshold:
                emblem, created = Badge.objects.get_or_create(name=name)
                if emblem not in user.badges.all():
                    user.badges.add(emblem)
                    user.badges_earned += 1  
                    user.save()



class AchievementsView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AchievementsSerializer

    def get_queryset(self):
        return Achievements.objects.all()

    def get(self, request, format=None):
        achievements = self.get_queryset()
        serializer = self.serializer_class(achievements, many=True)
        return Response(serializer.data)

class BadgeView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BadgeSerializer

    def get_queryset(self):
        return Badge.objects.all()

    def get(self, request, format=None):
        badge = self.get_queryset()
        serializer = self.serializer_class(badge, many=True)
        return Response(serializer.data)

class LeaderboardListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by('-assessment_count')
    serializer_class = LeaderboardSerializer

class NewMarkerSubmitView(APIView):
    
    def post(self, request, *args, **kwargs):
        markers_data = request.data.get('markers', [])
        if not markers_data:
            return Response({"error": "No markers data provided"}, status=status.HTTP_400_BAD_REQUEST)

        for marker_data in markers_data:
            serializer = NewMarkerSerializer(data={
                'latitude': marker_data['lat'],
                'longitude': marker_data['lng'],
                'description': marker_data.get('description', '')
            })
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Markers submitted successfully"}, status=status.HTTP_201_CREATED)

class DeleteMarkerSubmitView(APIView):
    def post(self, request, *args, **kwargs):
        markers_data = request.data.get('markers', [])

        if not isinstance(markers_data, list):
            return Response({"error": "Invalid format for markers data"}, status=status.HTTP_400_BAD_REQUEST)

        if not markers_data:
            return Response({"message": "No markers to process, but request was successful"}, status=status.HTTP_200_OK)

        created_count = 0
        for marker_id in markers_data:
            if not DeleteMarker.objects.filter(marker_id=marker_id).exists():
                DeleteMarker.objects.create(marker_id=marker_id)
                created_count += 1

        if created_count == 0:
            return Response({"message": "No new markers were added"}, status=status.HTTP_200_OK)

        return Response({"message": f"{created_count} markers added successfully"}, status=status.HTTP_201_CREATED)