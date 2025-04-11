from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from collection.views import add_starters

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collection = models.ManyToManyField('collection.Pokemon', blank=True, related_name='profile')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.username}"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = Profile.objects.create(user=instance)
            add_starters(profile)
            profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    class FriendRequest(models.Model):
        sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
        recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
        subject = models.CharField(max_length=240, blank=True)
        body = models.TextField(blank=True)
        timestamp = models.DateTimeField(auto_now_add=True)
        is_read= models.BooleanField(default=False)

        def __str__(self):
            return f"From {self.sender} to {self.recipient}: {self.subject}"