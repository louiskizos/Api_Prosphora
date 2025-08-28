from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer, LoginSerializer, ChurchSerializer, AbonnementSerializer, UserSerializer 
from .models import *
from .permissions import IsAbonnementValide
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import permissions



class RegisterView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = RegisterSerializer(user, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Utilisateur enregistré avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChurchListView(APIView):
    def get(self, request):
        churches = Church.objects.all()
        serializer = ChurchSerializer(churches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChurchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Église créée avec succès."}, status=201)
        return Response(serializer.errors, status=400)


class AbonnementCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAbonnementValide]

    def post(self, request):
        serializer = AbonnementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Abonnement créé."})
        return Response(serializer.errors, status=400)


# Vue de login avec informations supplémentaires
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        abonnement = Abonnement.objects.filter(eglise=user.eglise).order_by('-date').first()

        data.update({
            'user_id': user.id,
            'nom': user.nom,
            'email': user.email,
            'role': user.role,
            'eglise': user.eglise.nom,
            'abonnement_mois': abonnement.mois if abonnement else None,
            'abonnement_date': abonnement.date if abonnement else None,
        })
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
