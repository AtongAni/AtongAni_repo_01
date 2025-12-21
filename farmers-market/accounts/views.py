
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerRegisterSerializer, FarmerRegisterSerializer

class CustomerRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerRegisterSerializer

class FarmerRegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = FarmerRegisterSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
        })
    


