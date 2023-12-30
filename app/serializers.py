from rest_framework import serializers
from .models import Weather
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class WeatherApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ("id","city","temperature", "description", "icon", "updated_date", "api_response")
    
    def create(self, validated_data):
        ce = Weather(**validated_data)
        # print("Validated Data=========", **validated_data)        
        ce.save()
        return ce

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {
            "password":{"write_only":True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        # to save the password as hashed and crypted
        user.set_password(password)
        user.save()
        # for token based auth
        Token.objects.create(user=user)
        return user
    
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type":"password"},trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"),username=username, password=password)
        if not user:
            msg = "Credentials are not provided correctly..."
            raise serializers.ValidationError(msg, code="authentication")
        attrs["user"] = user
        return attrs

