from django.conf import settings
from django.db import models

# Create your models here.
class Game(models.Model):
    attacker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='games_started', on_delete=models.CASCADE)
    defender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='games_received', on_delete=models.CASCADE)

    attacker_card = models.IntegerField(default=0)
    defender_card = models.IntegerField(null=True, blank=True)

    winning_condition = models.CharField(
        max_length=10,
        choices=[('high', 'High wins'), ('low', 'Low wins')],
        default='high'
    )

    status = models.CharField(
        max_length=20,
        choices=[('waiting', 'Waiting'), ('finished', 'Finished')],
        default='waiting'
    )

    result = models.CharField(
        max_length=10,
        choices=[('attacker', 'Attacker Wins'), ('defender', 'Defender Wins'), ('draw', 'Draw')],
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)    
    