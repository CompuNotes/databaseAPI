# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class File(models.Model):
    path = models.CharField(max_length=255, db_collation='utf8mb4_bin')
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    tags = models.ManyToManyField(
        'Tag', through='FileTag')

    class Meta:
        managed = True
        db_table = 'FILE'

class Tag(models.Model):
    name = models.CharField(max_length=255, db_collation='utf8mb4_bin')

    class Meta:
        managed = True
        db_table = 'TAG'


class FileTag(models.Model):
    tag = models.ForeignKey(Tag, models.DO_NOTHING)
    file = models.ForeignKey(File, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'FILE_TAG'
        unique_together = (('tag', 'file'),)


class Rating(models.Model):
    rating = models.PositiveIntegerField()
    user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)  # The composite primary key (user_id, file_id) found, that is not supported. The first column is selected.
    file = models.ForeignKey(File, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'RATING'
        unique_together = (('user', 'file'),)


class User(models.Model):
    username = models.CharField(unique=True, max_length=255, db_collation='utf8mb4_bin')
    email = models.CharField(unique=True, max_length=255, db_collation='utf8mb4_bin')
    password = models.CharField(max_length=255, db_collation='utf8mb4_bin')

    class Meta:
        managed = True
        db_table = 'USER'
