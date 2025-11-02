from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings






# === Eglise ===
class Church(models.Model):
    nom = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    pasteur = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nom

# === Abonnement ===
class Abonnement(models.Model):
    eglise = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='abonnements')
    mois = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.eglise.nom} - {self.mois} mois"

# === User Manager ===
class CustomUserManager(BaseUserManager):

    def create_user(self, num_phone, password=None, **extra_fields):
        if not num_phone:
            raise ValueError("L'utilisateur doit avoir un numéro de téléphone.")
        user = self.model(num_phone=num_phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, num_phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')

        return self.create_user(num_phone, password, **extra_fields)

# === Custom User ===
class App_user(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('gestionnaire', 'Gestionnaire'),
        ('pasteur', 'Pasteur'),
        ('comptable', 'Comptable'),
        ('caissier', 'Caissier'),
    )

    eglise = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nom = models.CharField(max_length=100)
    num_phone = models.CharField(max_length=20,unique=True)
    date = models.DateField(default=timezone.now)

    is_active = True
    is_staff = False

    objects = CustomUserManager()

    USERNAME_FIELD = 'num_phone'
    REQUIRED_FIELDS = ['nom', 'role', 'eglise']

    def __str__(self):
        return self.num_phone


# === Groupe Offrandes ===
class Groupe_Offrandes(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_ordre = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    description_recette = models.CharField(max_length=100)
    
    def __str__(self):
        return self.description_recette


# === Sorte Offrande ===
class Sorte_Offrande(models.Model):
    id = models.AutoField(primary_key=True)
    descript_recette = models.ForeignKey(Groupe_Offrandes, on_delete=models.CASCADE)
    num_compte = models.CharField(max_length=20)
    nom_offrande = models.TextField(max_length=50)
    
    def __str__(self):
        return self.nom_offrande

    


# === Payement ===
class Payement_Offrande(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_offrande = models.ForeignKey(Sorte_Offrande, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100)
    type_payement = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    montant_lettre = models.CharField(max_length=255)
    type_monaie = models.CharField(max_length=100, default="CDF")
    motif = models.CharField(max_length=255,)
    date_payement = models.DateField()

# === Ahadi ===
class Ahadi(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom_offrande = models.ForeignKey(Sorte_Offrande, on_delete=models.CASCADE)
    nom_postnom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    montant_lettre = models.CharField(max_length=255)
    motif = models.CharField(max_length=255)
    type_monaie = models.CharField(max_length=100, default="CDF")
    date_ahadi = models.DateField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, default="1"
    )
  
    


# === Etat Besoin ===
class EtatBesoin(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.CharField(max_length=100)
    designation = models.CharField(max_length=255, default="Aucune désignation")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_monaie = models.CharField(max_length=100, default="CDF")
    quantite = models.CharField(max_length=100)
    motif = models.TextField()
    date_etat_besoin = models.DateField(auto_now_add=True)
    validation_pasteur = models.BooleanField(default=False)
    validation_caisse = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, default="1"
    )
    def __str__(self):
        return self.service





# === Groupe Previsions ===
class Groupe_Previsions(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_ordre = models.CharField(max_length=100)
    description_prevision = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, default="1"
    )
    def __str__(self):
        return self.num_ordre


# === Prevoir ===
class Prevoir(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descript_prevision = models.ForeignKey(Groupe_Previsions, on_delete=models.CASCADE)
    num_compte = models.BigIntegerField()
    nom_prevision = models.TextField(max_length=50)
    montant_prevus = models.DecimalField(max_digits=15, decimal_places=2)
    type_monaie = models.CharField(max_length=100, default="CDF")
    date_prevus = models.DateField(default=timezone.now)
    def __str__(self):
        return self.nom_prevision
    


