from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *



class PayementOffrandeSerializer(serializers.ModelSerializer):

    num_compte = serializers.CharField(source='nom_offrande.num_compte', read_only=True)
    nom_offrande_nom = serializers.CharField(source='nom_offrande.nom_offrande', read_only=True)

    class Meta:
        model = Payement_Offrande
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        eglise_id = kwargs.pop('eglise_id', None)
        super().__init__(*args, **kwargs)

        request = self.context.get('request', None)
        user = getattr(request, "user", None)

        if 'nom_offrande' in self.fields:
            if eglise_id:
                self.fields['nom_offrande'].queryset = (
                    self.fields['nom_offrande'].queryset.filter(
                        descript_recette__user__eglise_id=eglise_id
                    )
                )
            elif user and hasattr(user, "eglise") and user.eglise:
                self.fields['nom_offrande'].queryset = (
                    self.fields['nom_offrande'].queryset.filter(
                        descript_recette__user__eglise=user.eglise
                    )
                )




class ChurchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Church
        fields = '__all__'

class AbonnementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonnement
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = App_user
        exclude = ['password']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = App_user
        fields = ['id', 'num_phone', 'password', 'nom', 'role', 'eglise']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = App_user.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    num_phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(num_phone=data['num_phone'], password=data['password'])
        if user and user.is_active:
            abonnement = Abonnement.objects.filter(eglise=user.eglise).order_by('-date').first()
            return {
                'user_id': user.id,
                'nom': user.nom,
                'num_phone': user.num_phone,
                'role': user.role,
                'eglise': user.eglise.nom,
                'abonnement_mois': abonnement.mois if abonnement else None,
                'abonnement_date': abonnement.date if abonnement else None,
            }
        raise serializers.ValidationError("Numéro de téléphone ou mot de passe incorrect.")



class Groupe_OffrandesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe_Offrandes
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        eglise_id = self.context.get('eglise_id')
        if eglise_id:
            self.fields['user'].queryset = self.fields['user'].queryset.filter(eglise_id=eglise_id)
        else:
            self.fields['user'].queryset = self.fields['user'].queryset.none()


class Sorte_OffrandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorte_Offrande
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        eglise_id = kwargs.pop('eglise_id', None)
        super().__init__(*args, **kwargs)

        request = self.context.get('request', None)
        user = getattr(request, "user", None)

        if eglise_id:
            self.fields['descript_recette'].queryset = (
                self.fields['descript_recette'].queryset.filter(user__eglise_id=eglise_id)
            )
        elif user and hasattr(user, "eglise"):
            self.fields['descript_recette'].queryset = (
                self.fields['descript_recette'].queryset.filter(user__eglise=user.eglise)
            )


class Groupe_PrevisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe_Previsions
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        eglise_id = self.context.get('eglise_id')
        if eglise_id:
            self.fields['user'].queryset = self.fields['user'].queryset.filter(eglise_id=eglise_id)
        else:
            self.fields['user'].queryset = self.fields['user'].queryset.none()


class PrevoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prevoir
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        eglise_id = self.context.get('eglise_id')

        if eglise_id:
            self.fields['descript_prevision'].queryset = (
                self.fields['descript_prevision'].queryset.filter(user__eglise_id=eglise_id)
            )
        else:
            self.fields['descript_prevision'].queryset = self.fields['descript_prevision'].queryset.none()



class AhadiSerializer(serializers.ModelSerializer):
    
    total_paye = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    reste = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Ahadi
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        eglise_id = kwargs.pop('eglise_id', None)
        super().__init__(*args, **kwargs)

        request = self.context.get('request', None)
        user = getattr(request, "user", None)

        if eglise_id:
            self.fields['descript_recette'].queryset = (
                self.fields['descript_recette'].queryset.filter(user__eglise_id=eglise_id)
            )
        elif user and hasattr(user, "eglise"):
            self.fields['descript_recette'].queryset = (
                self.fields['descript_recette'].queryset.filter(user__eglise=user.eglise)
            )


class EtatBesoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatBesoin
        fields = '__all__'


# class Quarante_PourcentSerializer(serializers.ModelSerializer):
#     nom_offrande = serializers.CharField(source='nom_offrande.nom_offrande', read_only=True)

#     total_paye = serializers.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         read_only=True
#     )
#     # quarante_pourcent = serializers.DecimalField(
#     #     max_digits=15,
#     #     decimal_places=2,
#     #     read_only=True
#     # )


#     class Meta:
#         model = Quarante_Pourcent
#         fields = '__all__'
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         eglise_id = self.context.get('eglise_id')
#         if eglise_id:
#             self.fields['user'].queryset = self.fields['user'].queryset.filter(eglise_id=eglise_id)
#         else:
#             self.fields['user'].queryset = self.fields['user'].queryset.none()


# class Quarante_PourcentSerializer(serializers.ModelSerializer):
    
#     nom_offrande = serializers.CharField(source='nom_offrande.nom_offrande', read_only=True)

#     total_paye = serializers.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         read_only=True
#     )
#     quarante_pourcent = serializers.DecimalField(
#         max_digits=15,
#         decimal_places=2,
#         read_only=True
#     )

#     class Meta:
#         model = Quarante_Pourcent
#         fields = "__all__"

from rest_framework import serializers

class Quarante_PourcentSerializer(serializers.ModelSerializer):
    
    offrande = serializers.CharField(
        source='nom_offrande.nom_offrande',
        read_only=True
    )

    total_paye = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True
    )

    quarante_pourcent = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True
    )

    derniere_date_payement = serializers.DateTimeField(
        
        read_only=True
    )
#     derniere_date_payement = serializers.DateField(
#     source='date_payement',
#     read_only=True
# )

    class Meta:
        model = Quarante_Pourcent
        fields = [
            "id",
            "nom_offrande",        # ID de la FK
            "offrande",    # Nom lisible
            "total_paye",
            "quarante_pourcent",
            "derniere_date_payement",
            "user",
        ]
