from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from collection.views import add_starters

#
from django.contrib.auth.models import AbstractUser
#

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collection = models.ManyToManyField('collection.Pokemon', blank=True, related_name='profile')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    currency = models.PositiveBigIntegerField()

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

    def get_friends(user):
        sent = FriendRequest.objects.filter(from_user=user, is_accepted=True).values_list('to_user', flat=True)
        received = FriendRequest.objects.filter(to_user=user, is_accepted=True).values_list('from_user', flat=True)
        return User.objects.filter(id__in=list(sent) + list(received))

#
class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)
#

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # Prevent duplicate requests

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"



