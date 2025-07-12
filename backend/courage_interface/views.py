from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie  # This sets the CSRF cookie on GET requests
def get_csrf_token(request):
    # Endpoint just to set CSRF cookie, frontend calls this to fetch token.
    return Response({"csrfToken": get_token(request)})


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        data = request.data
        print(data)
        username = data.get('username',None)
        password = data.get('password',None)
        if not username or not password:
            return Response({"error": "Username and password required"}, status=200)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return Response({"message": "Login successful"},status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=200)
    except Exception as e:
        print(f"Error during login: {e}")
        return Response({"error": "An error occurred during login"}, status=500)