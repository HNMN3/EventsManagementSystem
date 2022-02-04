from django.urls import path

from events_management_system.events.views import (EventListView,
                                                   EventSubscriptionView)

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:event_id>/subscription/', EventSubscriptionView.as_view(),
         name='event-subscription'),
]
