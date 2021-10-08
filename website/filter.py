import django_filters
from django_filters import ChoiceFilter


from .models import  Type_choices


class PropertiesFilter(django_filters.FilterSet):
     Type_filter = ChoiceFilter(label='Type',field_name='Type',lookup_expr='icontains',choices=Type_choices)





