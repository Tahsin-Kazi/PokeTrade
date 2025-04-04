from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    pokemon = models.CharField(max_length=100)
    owner = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, default=1)
    image = models.URLField()
    date_collected = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)


    def __str__(self):
        return self.owner.user.username + "'s " + self.name