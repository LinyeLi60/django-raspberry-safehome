# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

from django.dispatch import receiver
from django.db.models.signals import post_save


class SensorType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


# Create your models here.
class Sensor(models.Model):
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sensor_type) + '-NO.' + str(self.id)


class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')  # 对原有用户进行拓展
    phone_regex = RegexValidator(regex=r'^1\d{10}$',
                                 message="Phone number must be entered in the format: '19876543237'.")
    telephone_number = models.CharField(max_length=11, blank=True, null=True, validators=[phone_regex])
    dialing_delay = models.IntegerField(default=20)  # 拨号延时
    is_stay = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
    else:
        instance.extension.save()
