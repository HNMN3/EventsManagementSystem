from django.contrib.auth.mixins import LoginRequiredMixin
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
    context_object_name = 'events'
    paginate_by = 30
    ordering = ['-start_date']


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
