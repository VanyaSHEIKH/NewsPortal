from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import *

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    date = DateFilter(field_name='date_in', lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Post
        fields = {
            'author':['exact'],
            'title':['icontains'],
       }