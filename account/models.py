from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

default_picture = 'no_image.jpg'
class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    current_place = models.CharField(max_length=30, blank=True)
    working_as = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default=default_picture, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    relationship_status = models.CharField(max_length=30, blank=True)
    interested_in = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    # Add your custom fields here

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def imageURL(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''
        return url

class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='to_user', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255)
    is_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} to {self.user}"

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content} from {self.receiver} {self.sender}"

