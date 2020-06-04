from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

def rename_and_upload(instance, filename):
    filebase, extension = filename.split('.')
    return 'user/{}_{}.{}'.format(instance.username, instance.id, extension)

class Video(models.Model):
    videoId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    tag = models.CharField(max_length=50)
    startTime = models.TimeField(default=':00:00')
    duration = models.IntegerField(default=60)

    class Meta:
        db_table = 'Video'

    def __str__(self):
        return self.title

class UserManager(BaseUserManager):
    def create_user(self, username, userFace):
        if not username:
            raise ValueError('Must be registered with a username')

        user = self.model(
            username=username,
            userFace=userFace,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, userFace,):
        user = self.create_user(
            username=username,
            userFace=userFace,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(
        max_length=100,
        unique=False,
    )
    userFace = models.ImageField(unique=True, upload_to=rename_and_upload)
    # ManyToMany
    videosSeen = models.ManyToManyField(Video, through='Result')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userFace'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Result(models.Model):
    resultId = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE
    )
    viewedDate = models.DateTimeField()
    dataPath = models.CharField(max_length=100)
    emotion = models.CharField(max_length=10)
    happiness = models.FloatField(null=True)
    sadness = models.FloatField(null=True)
    anger = models.FloatField(null=True)
    contempt = models.FloatField(null=True)
    disgust = models.FloatField(null=True)
    fear = models.FloatField(null=True)
    neutral = models.FloatField(null=True)
    surprise = models.FloatField(null=True)

    class Meta:
        db_table = 'Result'

    def __str__(self):
        return self.emotion