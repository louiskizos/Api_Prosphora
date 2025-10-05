from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from .models import *
from rest_framework import authentication, generics, mixins, permissions
from .permissions import IsAbonnementValide
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import permissions
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login


class Register_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
    ):
    

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return User.objects.filter(pk=pk)
        return User.objects.all()
    
    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)

class LoginView(APIView):
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            
            dernier_abonnement = user.eglise.abonnements.order_by('-date').first()

            response_data = {
                "user_id": user.id,
                "nom": user.nom,
                "email": user.email,
                "role": user.role,
                "eglise": user.eglise.nom if user.eglise else None,
                "abonnement_mois": dernier_abonnement.mois if dernier_abonnement else None,
                "abonnement_date": dernier_abonnement.date if dernier_abonnement else None
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": "Identifiants invalides."}, status=status.HTTP_401_UNAUTHORIZED)

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.validated_data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    
    def post(self, request):
        logout(request)
        return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)



class Church_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
    ):
    #permission_classes = [IsAuthenticated, IsAbonnementValide]
    
    queryset = Church.objects.all()
    serializer_class = ChurchSerializer
    lookup_field = 'pk'
    
    
    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Church.objects.filter(pk=pk)
        return Church.objects.all()
    



    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Église créée avec succès.", "data": serializer.data}, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)


# ====================== Abonnement =========================

class Abonnement_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = Abonnement.objects.all()
    serializer_class = AbonnementSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Abonnement.objects.filter(pk=pk)
        return Abonnement.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = AbonnementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Abonnement créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)

# ======================== GROUPE OFFRANDE =========================


class Groupe_Offrandes_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = Groupe_Offrandes.objects.all()
    serializer_class = Groupe_OffrandesSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Groupe_Offrandes.objects.filter(pk=pk)
        return Groupe_Offrandes.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = Groupe_OffrandesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Groupe d'offrande créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)
    
# ======================== SORTE OFFRANDE =========================

class Offrande_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = Sorte_Offrande.objects.all()
    serializer_class = Sorte_OffrandeSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        grp = self.kwargs.get('grp')
        if pk and grp:
            return Sorte_Offrande.objects.filter(descript_recette__user__eglise__id=pk, descript_recette__id=grp)
        if pk:
            return Sorte_Offrande.objects.filter(descript_recette__user__eglise__id=pk)
        if grp:
            return Sorte_Offrande.objects.filter(descript_recette__id=grp)
        return Sorte_Offrande.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        grp = kwargs.get('grp')
        if pk and grp:
            return self.list(request, *args, **kwargs)
        if pk is not None:
            return self.list(request, *args, **kwargs)
        if grp is not None:
            return self.list(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = Sorte_OffrandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Offrande créée."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)   
    
# ======================== GROUPE PREVISION =========================
class Groupe_Previsions_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = Groupe_Previsions.objects.all()
    serializer_class = Groupe_PrevisionsSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Groupe_Previsions.objects.filter(pk=pk)
        return Groupe_Previsions.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = Groupe_PrevisionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Groupe de prévision créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)
    
# ======================== PREVOIR =========================

class Prevoir_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = Prevoir.objects.all()
    serializer_class = PrevoirSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Prevoir.objects.filter(pk=pk)
        return Prevoir.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = PrevoirSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Prévoir créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)   