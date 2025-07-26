import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name="sender__username")
    date_after = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    date_before = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'date_after', 'date_before']
