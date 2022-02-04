from django.db import models
from django.utils import timezone

# Create your models here.


class EventManager(models.Manager):
    def upcoming(self):
        return self.filter(start_date__gt=timezone.now().date())

    def past(self):
        return self.filter(end_date__lt=timezone.now().date())

    def running(self):
        return self.filter(start_date__lte=timezone.now().date(),
                           end_date__gte=timezone.now().date())


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)
    users = models.ManyToManyField('users.User', related_name='events',
                                   blank=True)
    objects = EventManager()

    def __str__(self):
        return self.name

    @property
    def subscribed_users(self):
        return {user.id for user in self.users.all()}

    @property
    def can_subscribe(self):
        now = timezone.now().date()
        return now <= self.end_date
