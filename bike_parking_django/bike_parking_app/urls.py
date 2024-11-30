from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import views

# Define your URL patterns
urlpatterns = [ 
    # Add other custom endpoints
    # path('data/<str:Site_ID>/', views.BikeRackDataDetail.as_view(), name='data-detail'),  
    path('data/create/', views.BikeRackDataCreate.as_view(), name='data-create'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('user/', views.UserView.as_view(), name='user'),
    path('achievements/',views.AchievementsView.as_view(), name='achievements'),
    path('badge/',views.BadgeView.as_view(), name='badge'),
    path('leaderboard/', views.LeaderboardListView.as_view(), name='leaderboard'),
    path('verify-email/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='email-verify'),
    path('resend-verification-email/', views.resend_verification_email.as_view(), name='resend-verification-email'),
    path('password-reset-request/', views.PasswordResetRequest.as_view(), name='password_reset_request'),
    path('reset-password/<uidb64>/<token>/', views.SetNewPassword.as_view(), name='password_reset_confirm'),
    path('forgot-credentials/', views.ForgotCredentialsRequest.as_view(), name='forgot-credentials-request'),
    path('submit_newmarkers/', views.NewMarkerSubmitView.as_view(), name='submit_newmarkers'),
    # path('submit_Editmarkers/', views.EditMarkerPositionView.as_view(), name='submit_EditMarkerPositionView'),
    path('submit_deletemarkers/', views.DeleteMarkerSubmitView.as_view(), name='submit_deletemarkers'),
    path('create_assessment/', views.BikeRackDataView.as_view(), name='create_assessment'),
    # path('forgot-credentials-confirm/<uidb64>/<token>/', views.ForgotCredentialsConfirm.as_view(), name='forgot-credentials-confirm'),
    # path('reset-credentials/<uidb64>/<token>/', views.ResetCredentials.as_view(), name='reset-credentials'),
    ] 

