from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic.list import ListView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from events_management_system.events.models import Event


# Create your views here.
class EventListView(LoginRequiredMixin, ListView):
    """
    View for listing all events.
    """

    model = Event
    template_name = 'events/event_list.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """Generates queryset based on the tab selected (using query arguments)

        Returns:
            QuerySet: Generated queryset
        """
        list_type = self.request.GET.get('type', 'all')
        if list_type == 'upcoming':
            query = Event.objects.upcoming()
        elif list_type == 'past':
            query = Event.objects.past()
        elif list_type == 'running':
            query = Event.objects.running()
        else:
            query = Event.objects.all()
        return query.order_by('start_date', 'end_date')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add required context data for django template

        Returns:
            Dict[str, Any]: context data
        """
        context_data = super().get_context_data(**kwargs)
        print(context_data)
        context_data['list_type'] = self.request.GET.get('type', 'all')
        return context_data


class EventSubscriptionView(APIView):

    def post(self, request, event_id: int) -> Response:
        """Subscribe to an event.

        Args:
            request (request obj): request obj
            event_id (int): ID of the event

        Returns:
            Tuple[dict, int]: Tuple containing the response and status code
        """
        user = request.user
        event = Event.objects.get(id=event_id)
        event.users.add(user)
        event.save()
        response_data = {
            "message": "You have successfully subscribed to the event."
        }
        return Response(response_data, status=HTTP_200_OK)

    def delete(self, request, event_id: int) -> Response:
        """Unsubscribe from an event.

        Args:
            request (request obj): request obj
            event_id (int): ID of the event

        Returns:
            Tuple[dict, int]: Tuple containing the response and status code
        """
        user = request.user
        event = Event.objects.get(id=event_id)
        event.users.remove(user)
        event.save()
        response_data = {
            "message": "You have successfully unsubscribed from the event."
        }
        return Response(response_data, status=HTTP_200_OK)
