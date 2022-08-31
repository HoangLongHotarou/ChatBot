from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from .models import *
from django.db.models import Q


class CategoryFilter(FilterSet):
    parent_id = CharFilter(field_name='parent_id',lookup_expr='exact',method='include_null')
    
    def include_null(self, queryset, name, value):
        if value == 'null':
            return queryset.filter(
            Q(**{f'{name}__isnull': True})
        )
        else:
            return queryset.filter(**{name: value})

class AnswerFilter(FilterSet):
    class Meta:
        model = Answer
        fields = ('category_id','type_id')