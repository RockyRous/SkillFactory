from django.forms import DateInput
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Author, Category


class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains', field_name='title', label='Заголовок')
    author = ModelChoiceFilter(field_name='author', label='Имя автора', empty_label='Все авторы',
                               queryset=Author.objects.all())
    date_add = DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt',
                          field_name='date_add', label='Дата публикации позднее')
    category = ModelChoiceFilter(field_name='category', label='Категория', empty_label='Все категории',
                               queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'date_add',
            'category'
        ]