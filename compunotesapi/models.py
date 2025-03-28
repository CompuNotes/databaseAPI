from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.user.id, filename)

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


class User(models.Model):
    username = models.CharField(unique=True, max_length=255, blank=False, null=False)
    email = models.CharField(unique=True, max_length=255, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
