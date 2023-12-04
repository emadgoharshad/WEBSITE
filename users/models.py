from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager



class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username ')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        user.save()




def default_profile():
    return 'profile_default/profile_img_default.jpg'


def profile(self,filename):
    return f'profile_image/{self.pk}/profile_image.png'



class User(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=profile,default=default_profile,blank=True,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def get_profile(self):
        return str(self.get_profile)[str(self.get_profile).index('profile_image'+ str(self.pk) + "/"):]



    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True







