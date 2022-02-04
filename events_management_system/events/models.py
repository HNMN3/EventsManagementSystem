from django.db import models
from django.utils import timezone

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)
    users = models.ManyToManyField('users.User', related_name='events')

    def __str__(self):
        return self.name

    def is_subscribed_by_user(self, user_id):
        return self.users.filter(id=user_id).exists()

    def can_subscribe(self):
        now = timezone.now().date()
        return now <= self.end_date
