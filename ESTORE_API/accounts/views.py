from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate



# Create your views here.
class RootAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Root API Endpoint",
        operation_description="Provides the URLs for the available endpoints in the API.",
        responses={
            200: openapi.Response(
                'Successful operation',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                )
            )
        },
        tags=['Root']
    )
    def get(self, request, *args, **kwargs):
        api_urls = {
            'Customer Registration': '/api/register/',
        }
        return Response(api_urls, status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="User Registration",
        operation_description="Register a new user using email, name,phone number and password. A verification email will be sent.",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User registered successfully. Verification email sent.'),
            400: openapi.Response('Invalid data')
        },
        tags=['User Management']
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                user_data = RegisterSerializer(user).data
                # Optionally send verification email here
                return Response({
                    "message": "User registered successfully. Verification email sent.",
                    'user': user_data,
                    },status=status.HTTP_201_CREATED)
            except ValidationError as e:
                # Catch validation errors from the serializer or email sending
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Catch any unexpected errors
                return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
