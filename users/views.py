# views.py: Views for user registration
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserRegisterSerializer

# ViewSet for handling user registration
class RegisterView(viewsets.ViewSet):
    # Handles POST requests to register a new user
    def create(self, request):
        try:
            # Deserialize and validate incoming data
            serializer = UserRegisterSerializer(data=request.data)
            
            if serializer.is_valid():
                # Save the user if data is valid
                user = serializer.save()
                return Response({"id": user.id}, status=status.HTTP_201_CREATED)
                
            # Return validation errors if any
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # Catch-all for unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        