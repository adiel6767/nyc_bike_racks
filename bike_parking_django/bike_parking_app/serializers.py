import re
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import BikeRackData, Achievements, Badge, NewMarker, DeleteMarker

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        password = validated_data.get('password')


        user_obj = UserModel.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)

        return user_obj

class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    credentials = serializers.CharField()

    def check_user(self, clean_data):
        credentials = clean_data['credentials']
        password = clean_data['password']
        
        # Attempt authentication with username
        user = authenticate(username=credentials, password=password)
        
        # If authentication fails with username, attempt with email
        if user is None:
            try:
                user = UserModel.objects.get(email=credentials)
                user = authenticate(username=user.username, password=password)
            except UserModel.DoesNotExist:
                pass
        
        if user is None:
            try:
                user = UserModel.objects.get(phone_number=credentials)
                user = authenticate(username=user.username, password=password)
            except UserModel.DoesNotExist:
                pass
        
        if user is None:
            raise serializers.ValidationError('User not found or incorrect credentials. Please provide a valid username, email or phone number, and password')
        
        # Check if email is verified
        if not user.is_email_verified:
            raise serializers.ValidationError('Email is not verified. Please verify your email before logging in.')

        return user

class AchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievements
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'
   
class UserSerializer(serializers.ModelSerializer):
    achievements = AchievementsSerializer(many=True, read_only=True)
    badges = BadgeSerializer(many=True, read_only=True)
    phone_number = serializers.CharField(source='get_formatted_phone_number', read_only=True)    
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserModel
        fields = ['id','email', 'username','phone_number', 'achievements', 'image_id','assessment_count','assessment_ids','assessment_streak','distance_traveled','achievements_completed','badges_earned','mistery_boxes_earned','badges','is_email_verified','is_staff']

class BikeRackDataSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = BikeRackData
        fields = '__all__'

# class BikeRackDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BikeRackData
#         fields = ['rackType', 'condition', 'assessment', 'user', 'site_ID', 'newPosition', 'boroname', 'latitude', 'longitude', 'imageFile']
        
    def create(self, validated_data):
        # Save the file along with other data
        return BikeRackData.objects.create(**validated_data)

class LeaderboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['username','assessment_count']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not value[0].isupper():
            raise serializers.ValidationError("Password must start with a capital letter.")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain both letters and numbers.")
        return value

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        self.validate_password(password)
        
        return data

class NewMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewMarker
        fields = ['latitude', 'longitude', 'created_at']

class EditMarkerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewMarker
        fields = ['latitude', 'longitude', 'created_at']


# class DeleteMarkerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeleteMarker
#         fields = ['latitude', 'longitude', 'created_at']