from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from courage_interface.models import LoginAttempt
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie 
def get_csrf_token(request):
    return Response({"csrfToken": get_token(request)})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        data = request.data
        if request.user.is_authenticated:
            return Response({"message": "User already logged in","fullname":request.user.get_full_name()}, status=200)
        username = data.get('username',None)
        password = data.get('password',None)
        if not username or not password:
            return Response({"message": "Username and password required"}, status=200)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            last_attempt = LoginAttempt.objects.filter(user__username=username).last()
            if last_attempt and (last_attempt.retries <= 0):
                if last_attempt.retries <= 0 and last_attempt.last_attempt + timedelta(minutes=30) > timezone.now():
                    return Response({"message": "Too many login attempts. Please try again later."}, status=200)
            login(request, user)
            LoginAttempt.objects.create(
                user=user,
                was_success=True,
                retries=3, 
            ) 
            return Response({"message": "Login successful","fullname":user.get_full_name()},status=200)
        else:
            last_attempt = LoginAttempt.objects.filter(user__username=username).last()
            if last_attempt and last_attempt.retries > 0:
                last_attempt.retries -= 1
                last_attempt.was_success = False
                last_attempt.save()
            return Response({"message": "Invalid credentials"}, status=200)
    except Exception as e:
        return Response({"message": "An error occurred during login" + str(e)}, status=500)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    try:
        data = request.data
        first_name = data.get('name', '')
        username = data.get('username', None)
        password = data.get('password', None)
        if not username or not password:
            return Response({"message": "Username and password required"}, status=200)
        
        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already exists"}, status=200)
        
        user = User.objects.create_user(username=username, password=password,first_name=first_name)
        user.is_active = True
        user.save()
        LoginAttempt.objects.create(
            user=user,
            was_success=True,
            retries=3, 
        )
        login(request, user)
        return Response({"message": "User created successfully"}, status=201)
    except Exception as e:
        return Response({"message": "An error occurred during signup: " + str(e)}, status=500)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": "Logout successful"}, status=200)
        else:
            return Response({"message": "User not authenticated"}, status=200)
    except Exception as e:
        return Response({"message": "An error occurred during logout: " + str(e)}, status=500)