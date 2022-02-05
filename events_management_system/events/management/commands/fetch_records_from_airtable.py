from django.core.management.base import BaseCommand
import requests
from django.conf import settings
from events_management_system.events.models import Event


class Command(BaseCommand):
    def handle(self, *args, **options):
        headers = {
            'Authorization': f'Bearer {settings.AIRTABLE_API_KEY}',
        }
        event_objects = list()
        query_params = dict()
        while True:
            response = requests.get(
                f'{settings.AIRTABLE_API_URL}',
                headers=headers,
                params=query_params
            )
            response_json = response.json()
            for record in response_json['records']:
                airtable_event_data = record['fields']
                event_data = {
                    'name': airtable_event_data['Name'],
                    'description': airtable_event_data['Description'],
                    'start_date': airtable_event_data['Start Date'],
                    'end_date': airtable_event_data['End Date'],
                    'location': airtable_event_data['Location'],
                    'airtable_id': record['id']
                }

                event_obj = Event(**event_data)
                event_objects.append(event_obj)
            if response_json.get('offset') is None:
                break
            query_params['offset'] = response_json.get('offset')
        Event.objects.all().delete()
        Event.objects.bulk_create(event_objects)
        print("Airtable Data Synced")
