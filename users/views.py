from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import UserRegisterSerializer


class RegisterView(viewsets.ViewSet):
    def create(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.save()
                return Response({"id": user.id}, status=status.HTTP_201_CREATED)
                
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        