from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

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
    userFace = models.ImageField(unique=True, upload_to='user/')       # TODO : change to ByteString
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

class Video(models.Model):
    videoId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    tag = models.CharField(max_length=50)

    class Meta:
        db_table = 'Video'

    def __str__(self):
        return self.title
