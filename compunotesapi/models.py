from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return "{0}/{1}".format(instance.user.id, filename)

class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, blank=False, unique=True, null=False)
    title = models.CharField(max_length=255, blank=False, null=True, unique=True)
    user = models.ForeignKey('User', models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name='files', blank=True)

    class Meta:
        db_table = 'file'

    def __str__(self):
        if self.title is not None:
            return self.title
        return "Unknown title"


class Rating(models.Model):
    rating = models.DecimalField(max_digits=1,decimal_places=0, validators=[MaxValueValidator(5), MinValueValidator(1)])
    user_id = models.ForeignKey('User', models.CASCADE)
    file_id = models.ForeignKey('File', models.CASCADE)

    class Meta:
        db_table = 'rating'
        unique_together = (('user_id', 'file_id'),)

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255, blank=False, null=False)
    email = models.CharField(unique=True, max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'

    objects = UserManager()

    def __str__(self):
        return self.email
