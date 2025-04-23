from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from collection.views import add_starters

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    collection = models.ManyToManyField('collection.Pokemon', blank=True, related_name='profile')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    currency = models.PositiveBigIntegerField(default=1000)

    def __str__(self):
        return f"{self.user.username}"

    @receiver(post_save, sender=User)
    def create_or_save_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = Profile.objects.create(user=instance)
            add_starters(profile)
            profile.save()
        else:
            instance.profile.save()

    def get_friends(self):
        return self.friends.all()


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ])
    hidden_by_sender = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} ➝ {self.to_user} [{self.status}]"


def send_friend_request(from_user, to_user):
    if from_user != to_user and not FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        FriendRequest.objects.create(from_user=from_user, to_user=to_user)

def accept_friend_request(request_id):
    try:
        request = FriendRequest.objects.get(id=request_id)
        request.status = 'accepted'
        request.save()

        # Add each other as friends
        request.from_user.profile.friends.add(request.to_user)
        request.to_user.profile.friends.add(request.from_user)
    except FriendRequest.DoesNotExist:
        pass

def reject_friend_request(request_id):
    try:
        request = FriendRequest.objects.get(id=request_id)
        request.status = 'rejected'
        request.save()
    except FriendRequest.DoesNotExist:
        pass

