import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from events_management_system.events.models import Event
from tqdm import tqdm

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Running Events
        print("Creating Running Events")
        for i in tqdm(range(5)):
            event_obj = {
                "name": f"Event-{i}",
                "description": f"Description-{i}",
                "start_date": (timezone.now().date() -
                               timedelta(days=random.randint(1, 5))),
                "end_date": (timezone.now().date() +
                             timedelta(days=random.randint(1, 5))),
                "location": f"Location-{i}"
            }
            Event.objects.create(**event_obj)
        # Past Events
        print("Creating Past Events")
        for i in tqdm(range(5, 10)):
            event_obj = {
                "name": f"Event-{i}",
                "description": f"Description-{i}",
                "start_date": (timezone.now().date() -
                               timedelta(days=random.randint(5, 10))),
                "end_date": (timezone.now().date() -
                             timedelta(days=random.randint(1, 5))),
                "location": f"Location-{i}"
            }
            Event.objects.create(**event_obj)
        # Future Events
        print("Creating Future Events")
        for i in tqdm(range(10, 15)):
            event_obj = {
                "name": f"Event-{i}",
                "description": f"Description-{i}",
                "start_date": timezone.now().date() + timedelta(days=random.randint(1, 5)),
                "end_date": timezone.now().date() + timedelta(days=random.randint(5, 10)),
                "location": f"Location-{i}"
            }
            Event.objects.create(**event_obj)

        print("Sample events created successfully")
