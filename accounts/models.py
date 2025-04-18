from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from collection.views import add_starters

#
from django.contrib.auth.models import AbstractUser
#

from django.conf import settings
from django.utils import timezone

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

#     def get_friends(user):
#         sent = FriendRequest.objects.filter(from_user=user, is_accepted=True).values_list('to_user', flat=True)
#         received = FriendRequest.objects.filter(to_user=user, is_accepted=True).values_list('from_user', flat=True)
#         return User.objects.filter(id__in=list(sent) + list(received))
#
# # #
# # class User(AbstractUser):
# #     friends = models.ManyToManyField("User", blank=True)
# # #
#
# class FriendRequest(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     ]
#
#
#     from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
#
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ('from_user', 'to_user')  # Prevent duplicate requests
#
#     def __str__(self):
#         return f"{self.from_user} -> {self.to_user}"

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend
        """
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        Remove a friend
        """

        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Initiate the action of unfriending someone.
        """
        remover_friends_list = self # person terminating the friendship

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        """
        Is this a friend?
        """
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """
    A friend request consists of two main parts:
        1. SENDER:
            - Person sending/initiating the friend request
        2. RECIEVER:
            - Person receiving the friend request
    """

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

    is_active = models.BooleanField(blank=True, null=False, default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept the friend request
        Update both SENDER and RECIEVER friend lists
        """

        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request
        Is it "declined" by setting the 'is_active' field to False
        """

        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancel a friend request
        It is 'canceled' by setting the 'is_active' field to False.
        This is only different with respect to "declining" through the notification that is generated.
        """

        self.is_active = False
        self.save()


