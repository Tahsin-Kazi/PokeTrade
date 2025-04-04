from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from collection.models import Pokemon


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collection = models.ManyToManyField('collection.Pokemon', blank=True, related_name='profile')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.username}"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except:
            Profile.objects.create(user=instance)