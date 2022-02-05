import requests
from django.conf import settings
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
    airtable_id = models.CharField(max_length=100, blank=True)
    objects = EventManager()

    def __str__(self):
        return self.name

    @property
    def subscribed_users(self):
        return {user.id for user in self.users.all()}

    @property
    def airtable_serialize(self):
        return {
            'Name': self.name,
            'Description': self.description,
            'Start Date': self.start_date.strftime('%Y-%m-%d'),
            'End Date': self.end_date.strftime('%Y-%m-%d'),
            'Location': self.location,
        }

    @property
    def can_subscribe(self):
        now = timezone.now().date()
        return now <= self.end_date

    def create_record_on_airtable(self):
        """ Create a new record on Airtable"""
        headers = {
            'Authorization': f'Bearer {settings.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {"fields": self.airtable_serialize}
        response = requests.post(
            settings.AIRTABLE_API_URL,
            json=data,
            headers=headers
        )
        if response.status_code != 200:
            raise Exception(response.json())
        self.airtable_id = response.json()['id']

    def update_record_on_airtable(self):
        """ Update an existing record on Airtable"""
        headers = {
            'Authorization': f'Bearer {settings.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {"fields": self.airtable_serialize}
        response = requests.patch(
            f'{settings.AIRTABLE_API_URL}/{self.airtable_id}',
            json=data,
            headers=headers
        )
        if response.status_code != 200:
            raise Exception(response.json())

    def delete_record_on_airtable(self):
        """Delete a record from Airtable
        """
        headers = {
            'Authorization': f'Bearer {settings.AIRTABLE_API_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.delete(
            f'{settings.AIRTABLE_API_URL}/{self.airtable_id}',
            headers=headers
        )
        if response.status_code != 200:
            raise Exception(response.json())

    def save(self, *args, **kwargs) -> None:
        """ Override save method to push changes on Airtable
        """

        # Push changes to AirTable
        if self.pk is None:
            self.create_record_on_airtable()
        else:
            self.update_record_on_airtable()

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        """
        """
        self.delete_record_on_airtable()
        super().delete(*args, **kwargs)
