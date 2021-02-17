import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
#from jwt.compat import text_type
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.six import text_type
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import User, ActivityPeriod
USER_LIFETIME = datetime.timedelta(days=30)

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def save(self):
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs['email']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        activecheck = User.objects.filter(email=username).filter(is_active=0)
        if activecheck.exists():
            custom = {"error": "Please verify email", "status": "0"}
            return custom
        if not user:
            custom={"error":"Invalid Credentials","status":"0"}
            return custom
        data = super(TokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        if self.user.is_superuser:
            new_token = refresh.access_token
            new_token.set_exp(lifetime=USER_LIFETIME)
            data['access'] = text_type(new_token)
            token, _ = Token.objects.get_or_create(user=user)
        else:
            data['access'] = text_type(refresh.access_token)
        data['user details'] = self.user.email
        return data


class TokenObtainPairPatchedSerializer(object):
    pass