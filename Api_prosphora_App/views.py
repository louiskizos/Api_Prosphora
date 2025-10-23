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
from django.db.models import Sum, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q, OuterRef, Subquery, Sum
from decimal import Decimal

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
        num_phone = request.data.get("num_phone")
        password = request.data.get("password")
        print(f"Login attempt: num_phone={num_phone}, password={'*' * len(password) if password else None}")

        user = authenticate(request, num_phone=num_phone, password=password)

        if user is not None:
            login(request, user)

            
            dernier_abonnement = user.eglise.abonnements.order_by('-date').first()

            response_data = {
                "user_id": user.id,
                "nom": user.nom,
                "num_phone": user.num_phone,
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

    queryset = Sorte_Offrande.objects.all()
    serializer_class = Sorte_OffrandeSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        grp = self.kwargs.get('grp')
        if pk and grp:
            return Sorte_Offrande.objects.filter(descript_recette__user__eglise__id=pk, descript_recette__id=grp)
        if pk:
            return Sorte_Offrande.objects.filter(id=pk)
        if grp:
            return Sorte_Offrande.objects.filter(descript_recette__id=grp)
        return Sorte_Offrande.objects.all()
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        grp = kwargs.get('grp')
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
    


# ======================== PAYEMENT =========================

class Payement_Offrande_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = Payement_Offrande.objects.all()
    serializer_class = PayementOffrandeSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return Payement_Offrande.objects.filter(pk=pk)
        return Payement_Offrande.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = PayementOffrandeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Payement créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)   


# ======================== AHADI =========================

class Ahadi_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    queryset = Ahadi.objects.all()
    serializer_class = AhadiSerializer
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Liste tous les engagements (Ahadi) avec le total payé et le reste à payer.
        Si un 'pk' est fourni, retourne un seul objet.
        """

        pk = kwargs.get('pk')
        engagements = self.get_queryset()

        if pk:
            engagements = engagements.filter(pk=pk)

        paiements = (
            Payement_Offrande.objects.filter(
                type_payement="Entree",
                nom_offrande=OuterRef('nom_offrande'),
                departement=OuterRef('nom_postnom'),
                nom_offrande__descript_recette__description_recette="Les engagements des adhérents"
            )
            .values('nom_offrande', 'departement')
            .annotate(total_paye=Sum('montant'))
            .values('total_paye')
        )

        engagements = engagements.annotate(
            total_paye=Subquery(paiements, output_field=models.DecimalField(max_digits=15, decimal_places=2))
        )

        for e in engagements:
            e.reste = (e.montant or Decimal('0')) - (e.total_paye or Decimal('0'))

        serializer = self.get_serializer(engagements, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ahadi créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        
        return self.destroy(request, *args, **kwargs)


# ======================== ETAT DE BESOIN =========================
class EtatBesoin_Mixins(
    generics.GenericAPIView,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):

    #permission_classes = [IsAuthenticated,]


    queryset = EtatBesoin.objects.all()
    serializer_class = EtatBesoinSerializer
    lookup_field = 'pk'
    

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk:
            return EtatBesoin.objects.filter(pk=pk)
        return EtatBesoin.objects.all()
    


    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)
    
    def post(self, request):
        serializer = EtatBesoinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Etat de besoin créé."})
        return Response(serializer.errors, status=400)
    
    def put(self, request, *args, **kwargs):

        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)

# ======================== Rapport Bilan =========================   

class BilanAPIView(APIView):
    """
    API view qui retourne un bilan détaillé des prévisions et paiements.
    """

    def get(self, request):

        prevision_qs = Prevoir.objects.select_related('descript_prevision')
        paiement_qs = Payement_Offrande.objects.select_related('nom_offrande')


        # Agrégation des prévisions
        grouped = prevision_qs.values(
            'descript_prevision__num_ordre',
            'descript_prevision__description_prevision',
            'annee_prevus'
        ).annotate(total_prevus=Sum('montant_prevus')).order_by('descript_prevision__num_ordre', 'annee_prevus')

        # Traitement des données
        combined_data = []
        for group in grouped:
            num_ordre = group['descript_prevision__num_ordre']
            annee = group['annee_prevus']

            # Récupérer les prévisions liées à ce groupe
            related_data = prevision_qs.filter(
                descript_prevision__num_ordre=num_ordre,
                annee_prevus=annee
            ).values('nom_prevision', 'num_compte', 'montant_prevus')

            # Récupérer les paiements
            pay_qs_filtered = paiement_qs.filter(
                nom_offrande__descript_recette__num_ordre=num_ordre,
                annee=annee
            )

            # Agrégation des paiements
            pay_grouped = pay_qs_filtered.values(
                'nom_offrande__num_compte',
                'nom_offrande__nom_offrande'
            ).annotate(
                total_recette=Sum('montant', filter=Q(type_payement='Entree')),
                total_depense=Sum('montant', filter=Q(type_payement='Sortie')),
            )

            # Fusionner les prévisions et paiements
            prevision_list = [{
                'libelle': item['nom_prevision'],
                'num_compte': item['num_compte'],
                'recette': '-',
                'depense': '-',
                'prevision': item['montant_prevus'],
            } for item in related_data]

            paiement_list = [{
                'libelle': item['nom_offrande__nom_offrande'],
                'num_compte': item['nom_offrande__num_compte'],
                'recette': item['total_recette'] or '-',
                'depense': item['total_depense'] or '-',
                'prevision': '-',
            } for item in pay_grouped]

            lignes_fusionnees = prevision_list + paiement_list

            total_recettes = sum(
                [p['recette'] if p['recette'] != '-' else 0 for p in paiement_list], Decimal(0)
            )
            total_depenses = sum(
                [p['depense'] if p['depense'] != '-' else 0 for p in paiement_list], Decimal(0)
            )

            combined_data.append({
                'num_ordre': num_ordre,
                'description_prevision': group['descript_prevision__description_prevision'],
                'annee_prevus': annee,
                'total_prevus': group['total_prevus'] or 0,
                'total_recettes': total_recettes,
                'total_depenses': total_depenses,
                'lignes': lignes_fusionnees
            })


        data_filtered = EtatBesoin.objects.filter(validation_pasteur=True)
        data_etat_counter = data_filtered.count()

        data_filteredFalse = EtatBesoin.objects.filter(validation_pasteur=False)
        data_etat_counter_P = data_filteredFalse.count()

        context = {
            'data_etat_count_C': data_etat_counter,
            'data_etat_besoin_true': data_filtered.values(),
            'data_etat_besoin_false': data_filteredFalse.values(),
            'data_etat_count_P': data_etat_counter_P,
            'data': combined_data
        }

        return Response(context, status=status.HTTP_200_OK)



# =================== Rapport prevision =======================================
