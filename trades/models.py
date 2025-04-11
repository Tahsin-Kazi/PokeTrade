from django.db import models

class Trade(models.Model):

    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('countered', 'Countered'),
        ('canceled', 'Canceled'),
    ]

    sender = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="sender_trade")
    receiver = models.ForeignKey("accounts.profile", on_delete=models.CASCADE, related_name="receiver_trade")
    sender_pokemon = models.ManyToManyField('collection.Pokemon', blank=True, related_name='sender_pokemon_trade')
    receiver_pokemon = models.ManyToManyField('collection.Pokemon', blank=True, related_name='receiver_pokemon_trade')
    date_posted = models.DateField(auto_now=True)
    status = models.CharField(max_length=100, choices=status_choices, default='pending')

    def __str__(self):
        return f"Trade #{self.id} - {self.sender.user.username} to {self.receiver.user.username}"