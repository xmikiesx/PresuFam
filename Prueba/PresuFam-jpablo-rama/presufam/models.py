from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from datetime import datetime
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, unique=True)  # user email

    nombre = models.CharField(max_length=30, validators=[
        RegexValidator(regex='^[a-zA-Z\s]*$', message='El nombre sólo puede contener letras.', code='invalid_name')])

    apellido = models.CharField(max_length=50, validators=[
        RegexValidator(regex='^[a-zA-Z\s]*$', message='El nombre sólo puede contener letras.', code='invalid_last_name')])

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def get_full_name(self):
        cad = "{0} {1}"
        return cad.format(self.nombre, self.apellido)

    def __str__(self):  # print
        cad = "{0} {1}, {2}"
        return cad.format(self.nombre, self.apellido, self.email)


class Category(models.Model):
    nombre = models.CharField(max_length=30, validators=[
        RegexValidator(regex='^[a-zA-Z]*$', message='El nombre sólo puede contener letras.', code='invalid_name')])
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    create_on = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('presufam:detail', kwargs={'pk': self.pk})

    @classmethod
    def create(cls, nombre, user):
        categoria = cls(name=nombre, user=user)
        return categoria

    def __str__(self):
        return self.nombre


class Income(models.Model):
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.001)])
    nombre = models.CharField(max_length=20, validators=[
        RegexValidator(regex='^[\w\s]*$', message='El nombre sólo puede contener letras.', code='invalid_name'),
    ])
    fecha = models.DateField(default=datetime.now)


class Expense(models.Model):
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.001)])
    nombre = models.CharField(max_length=20, validators=[
        RegexValidator(regex='^[\w\s]*$', message='El nombre sólo puede contener letras.', code='invalid_name'),
    ])
    fecha = models.DateField(default=datetime.now)

