from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from knox.views import LoginView as KnoxLoginView
from . serializers import RegisterSerializer, UserSerializer, CustomAuthTokenSerializer
from rest_framework.response import Response
from knox.models import AuthToken


User = get_user_model()

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """ User login """
        serializer = CustomAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
            API that register a user in two databases, the erp_database and the django local database
        """
        #
        # # Serialize request data with RegisterSerializer
        #
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()    

        #
        # # Serialize the user to be returned in the response with its token
        #
        user_ = UserSerializer(user, context=self.get_serializer_context()).data
        return Response({
            "user": user_,
            "token": AuthToken.objects.create(user)[1]
        })
