from rest_framework import serializers
from rest_framework import serializers
from .models import Church, Abonnement, User
from django.contrib.auth import authenticate

from .models import *

# Sérialiseur pour Payement_Offrande
class PayementOffrandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payement_Offrande
        fields = ['nom_offrande', 'departement', 'montant', 'date_payement', 'annee']

# Sérialiseur pour Prevoir
class PrevoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prevoir
        fields = ['descript_prevision', 'montant_prevus', 'annee_prevus']



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
        model = User
        exclude = ['password']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'num_phone', 'password', 'nom', 'role', 'eglise']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
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

class Sorte_OffrandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorte_Offrande
        fields = '__all__'

class Groupe_PrevisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groupe_Previsions
        fields = '__all__'


class PrevoirSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prevoir
        fields = '__all__'
