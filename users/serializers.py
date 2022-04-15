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
        #fields =  '__all__'
        exclude = ('password', )
        #fields = ('id', 'phone_number', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password')
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['phone_number'], validated_data['password'])

        return user
