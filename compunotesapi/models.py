from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class File(models.Model):
    path = models.FilePathField(max_length=255, blank=False, null=False, unique=True, path='/home/compunotes/files', recursive=True)
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
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user_id = models.ForeignKey('User', models.CASCADE)
    file_id = models.ForeignKey('File', models.CASCADE)

    class Meta:
        db_table = 'rating'
        unique_together = (('user_id', 'file_id'),)


class User(models.Model):
    username = models.CharField(unique=True, max_length=255, blank=False, null=False)
    email = models.CharField(unique=True, max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
