from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

User = get_user_model()

class CustomAuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label=_("phone_number"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                username=phone_number, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone_number" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'country_code', 'phone_number', 'gender', 'birthdate',)


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'country_code', 'phone_number', 'password' ,'gender', 'birthdate','avatar', 'email',)
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        first_name = validated_data.get('first_name') or None
        last_name = validated_data.get('last_name') or None
        country_code = validated_data.get('country_code') or None
        gender = validated_data.get('gender') or None
        birthdate = validated_data.get('birthdate') or None
        avatar = validated_data.get('avatar') or None
        email = validated_data.get('email') or None

        user = User.objects.create_user(
                    phone_number = phone_number, 
                    password = password, 
                    first_name = first_name, 
                    last_name = last_name, 
                    country_code = country_code, 
                    gender = gender, 
                    birthdate = birthdate, 
                    avatar = avatar, 
                    email = email, 
                )

        return user
