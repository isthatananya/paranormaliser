from datetime import timedelta
from django.utils import timezone
from ai_integration.models import ChatHistory, ModelAccessHistory
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def save_conversation(request):
    try:
        data = request.data
        username = data.get('username')
        user_question = data.get('user_question')
        model_response = data.get('model_response')
        is_parent = data.get('is_parent', False)
        parent_chat_id = data.get('parent_chat_id', None)
        model_name = data.get('model_name', 'default_model')
        
        user_id = User.objects.filter(username=username).id
        
        if not user_id or not user_question or not model_response:
            return Response({"message": "User ID, question, and response are required"}, status=400)
        
        model_access = ModelAccessHistory.objects.get_or_create(accessed_by=user_id)
        model_access.model_name = model_name
        model_access.access_time = timezone.now()
        model_access.attempts_count -= 1
        model_access.save()
        
        chat_history = ChatHistory.objects.create(
            user_id=user_id,
            user_question=user_question,
            model_response=model_response,
            is_parent=is_parent,
            parent_chat_id=parent_chat_id 
        )
        
        return Response({"message": "Conversation saved successfully", "chat_id": chat_history.id}, status=201)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    except Exception as e:
        return Response({"message": "An error occurred: " + str(e)}, status=500)