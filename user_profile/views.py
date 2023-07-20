from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# model imports
from .models import UserProfile
# serializer imports
from .serlializers import UserSerializer

class GetLoggedInUserData(APIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):
        user = request.user
        
        user_serializer = UserSerializer(user, many=False)

        return Response(user_serializer.data)